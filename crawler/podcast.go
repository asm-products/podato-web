package crawler

import (
	rss "github.com/jteeuwen/go-pkg-rss"
	"sort"
	"strconv"
	"strings"
	"time"
)

//Explicitness constants
const (
	explUndefined = iota
	explClean     = iota
	explExplicit  = iota
)

type Podcast struct {
	Url         string    `datastore:"-"`
	Title       string    `datastore:"title"`
	Author      string    `datastore:"author"`
	Description string    `datastore:"description,noindex"`
	Language    string    `datastore:"language"`
	Copyright   string    `datastore:"copyright"`
	Image       string    `datastore:"image,noindex"`
	Categories  []string  `datastore:"categories"`
	Owner       Person    `datastore:"owner,noindex"`
	Episodes    []Episode `datastore:"episodes"`
	LastFetched time.Time `datastore:"last_fetched",noindex`
	MovedTo     string    `datastore:"moved_to,noindex"`
	Complete    bool      `datastore:"complete"`
	Hub         string    `datastore:"hub"` //pubsubhubbub hub, for efficient crawling
}

type Person struct {
	Name  string `datastore:"name,noindex"`
	Email string `datastore:"email,noindex"`
}

type Episode struct {
	Title       string    `datastore:"title,noindex"`
	Subtitle    string    `datastore:"subtitle,noindex"`
	Description string    `datastore:"description,noindex"`
	Author      string    `datastore:"author,noindex"`
	Guid        string    `datastore:"guid"`
	Published   time.Time `datastore:"published"`
	Image       string    `datastore:"image,noindex"`
	Duration    int       `datastore:"duration,noindex"`
	Explicit    int8      `datastore:"explicit"`
	Order       int       `datastore:"-"`
}

func (p *Podcast) UpdateFromFeed(f *rss.Feed) {
	p.Url = f.Url
	p.UpdateFromChannel(f.Channels[0])
}

func (p *Podcast) UpdateFromChannel(c *rss.Channel) {
	complete, _ := strconv.ParseBool(safelyGetFirstExtension(getItunesExtensions(c)["complete"]).Value)
	p.Title = c.Title
	p.Author = safelyGetFirstExtension(getItunesExtensions(c)["author"]).Value
	p.Description = getPodcastDescription(c)
	p.Language = c.Language
	p.Copyright = c.Copyright
	p.Image = getPodcastImage(c)
	p.Categories = getPodcastCategories(c)
	p.Owner = getPodcastOwner(c)
	p.LastFetched = time.Now()
	p.MovedTo = safelyGetFirstExtension(getItunesExtensions(c)["new-feed-url"]).Value
	p.Complete = complete
	p.Episodes = episodesFromItems(c.Items)
}

func episodesFromItems(items []*rss.Item) []Episode {
	episodes := make([]Episode, len(items))
	for i, e := range items {
		episodes[i] = episodeFromItem(e)
	}
	sortEpisodes(episodes)
	return episodes
}

func episodeFromItem(e *rss.Item) Episode {
	pd, _ := e.ParsedPubDate()
	o, _ := strconv.ParseInt(safelyGetFirstExtension(getItemItunesExtensions(e)["order"]).Value, 10, 0)
	order := int(o)
	return Episode{
		Title:       e.Title,
		Subtitle:    safelyGetFirstExtension(getItemItunesExtensions(e)["subtitle"]).Value,
		Description: getEpisodeDescription(e),
		Author:      safelyGetFirstExtension(getItemItunesExtensions(e)["author"]).Value,
		Guid:        e.Key(),
		Published:   pd,
		Image:       getEpisodeImage(e),
		Duration:    getEpisodeDuration(e),
		Explicit:    getEpisodeExplicit(e),
		Order:       order,
	}
}

func sortEpisodes(eps []Episode) {
	es := episodeSorter{eps}
	sort.Sort(es)
}

type episodeSorter struct {
	episodes []Episode
}

func (e episodeSorter) Len() int {
	return len(e.episodes)
}

func (e episodeSorter) Less(i, j int) bool {
	e1 := e.episodes[i]
	e2 := e.episodes[j]
	if e1.Order != e2.Order {
		return e1.Order < e2.Order
	} else {
		return e1.Published.Before(e2.Published)
	}
}

func (e episodeSorter) Swap(i, j int) {
	e.episodes[i], e.episodes[j] = e.episodes[j], e.episodes[i]
}

func getItunesExtensions(c *rss.Channel) map[string][]rss.Extension {
	return c.Extensions["http://www.itunes.com/dtds/podcast-1.0.dtd"]
}

func getItemItunesExtensions(i *rss.Item) map[string][]rss.Extension {
	return i.Extensions["http://www.itunes.com/dtds/podcast-1.0.dtd"]
}

func safelyGetFirstExtension(es []rss.Extension) rss.Extension {
	if len(es) > 0 {
		return es[0]
	}
	return rss.Extension{}
}

func getPodcastDescription(c *rss.Channel) string {
	itunes := safelyGetFirstExtension(getItunesExtensions(c)["summary"]).Value
	if itunes != "" {
		return itunes
	}
	return c.Description
}

func getPodcastImage(c *rss.Channel) string {
	itunes := safelyGetFirstExtension(getItunesExtensions(c)["image"]).Attrs["href"]
	if itunes != "" {
		return itunes
	}
	return c.Image.Url
}

func getPodcastCategories(c *rss.Channel) []string {
	cs := getItunesCategories(getItunesExtensions(c))
	return append(cs, categoriesToStrings(c.Categories)...)
}

func categoriesToStrings(cs []*rss.Category) []string {
	s := make([]string, len(cs))
	for i, c := range cs {
		s[i] = c.Text
	}
	return s
}

func getItunesCategories(es map[string][]rss.Extension) []string {
	cats := es["category"]
	s := make([]string, len(cats))

	for i, c := range cats {
		s[i] = c.Attrs["text"]
	}
	return s
}

func getPodcastOwner(c *rss.Channel) Person {
	owner := safelyGetFirstExtension(getItunesExtensions(c)["owner"])
	return Person{
		Name:  safelyGetFirstExtension(owner.Childrens["name"]).Value,
		Email: safelyGetFirstExtension(owner.Childrens["email"]).Value,
	}
}

func getEpisodeDescription(i *rss.Item) string {
	summary := safelyGetFirstExtension(getItemItunesExtensions(i)["summary"]).Value
	if summary == "" {
		summary = i.Description
	}
	return summary
}

func getEpisodeImage(i *rss.Item) string {
	return safelyGetFirstExtension(getItemItunesExtensions(i)["image"]).Attrs["href"]
}

func getEpisodeDuration(i *rss.Item) int {
	strDur := safelyGetFirstExtension(getItemItunesExtensions(i)["duration"]).Value
	parts := strings.Split(strDur, ":")
	var hrs, mins, secs int64
	if len(parts) == 0 {
		return 0
	} else if len(parts) == 1 {
		secs, _ = strconv.ParseInt(parts[0], 10, 0)
	} else if len(parts) == 2 {
		mins, _ = strconv.ParseInt(parts[0], 10, 0)
		secs, _ = strconv.ParseInt(parts[1], 10, 0)
	} else {
		l := len(parts)
		secs, _ = strconv.ParseInt(parts[l-1], 10, 0)
		mins, _ = strconv.ParseInt(parts[l-2], 10, 0)
		hrs, _ = strconv.ParseInt(parts[l-3], 10, 0)
	}

	return int(secs + 60*mins + 3600*hrs)
}

func getEpisodeExplicit(i *rss.Item) int8 {
	exp := safelyGetFirstExtension(getItemItunesExtensions(i)["explicit"]).Value
	var e int8
	switch exp {
	case "yes":
		e = explExplicit
	case "clean":
		e = explClean
	default:
		e = explUndefined
	}
	return e
}
