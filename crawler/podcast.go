package crawler

import (
	"time"
	"sort"
	rss"github.com/jteeuwen/go-pkg-rss"
)

type Podcast struct {
	Url string `datastore:"-"`
	Title string `datastore:"title"`
	Author string `datastore:"author"`
	Description string `datastore:"description,noindex"`
	Language string `datastore:"language"`
	Copyright string `datastore:"copyright"`
	Image string `datastore:"image,noindex"`
	Categories []string `datastore:"categories"`
	Owner Person `datastore:"owner,noindex"`
	Episodes []Episode `datastore:"episodes"`
	LastFetched time.Time `datastore:"last_fetched",noindex`
	MovedTo string `datastore:"moved_to,noindex"`
	Complete bool `datastore:"complete"`
	Hub string `datastore:"hub"` //pubsubhubbub hub, for efficient crawling
}

type Person struct {
	Name string `datastore:"name,noindex"`
	Email string `datastore:"email,noindex"`
}

type Episode struct {
	Title string `datastore:"title,noindex"`
	Subtitle string `datastore:"subtitle,noindex"`
	Description string `datastore:"description,noindex"`
	Author string `datastore:"author,noindex"`
	Categories []string `datastore:"categories"`
	Guid string `datastore:"guid"`
	Published time.Time `datastore:"published"`
	Image string `datastore:"image,noindex"`
	Duration int `datastore:"duration,noindex"`
	Explicit bool `datastore:"explicit"`
	Likes int32 `datastore:"likes,noindex"`
	Dislikes int32 `datastore:"dislikes,noindex"`
	Views int32 `datastore:"views"`
	Order int `datastore:"-"`
}

func (p *Podcast) UpdateFromFeed(f *rss.Feed) {
	p.Url = f.Url
	p.UpdateFromChannel(p.Channels[0])
}

func (p *Podcast) UpdateFromChannel(c *rss.Channel) {
	p.Title = c.Title
	p.Author = getItunesExtensions(c)["author"][0].Value
	p.Description = getPodcastDescription(c)
	p.Language = c.Language
	p.Copyright = c.Copyright
	p.Image = getPodcastImage(c)
	p.Categories = getPodcastCategories(c)
	p.Owner = getPodcastOwner(c)
	p.LastFetched = time.Now()
	p.MovedTo = getItunesExtentions(c)["new-feed-url"][0].Value
	p.Complete = getItunesExtensions(c)["complete"][0].Value
	p.Hub = getPodcastHub(c)
	p.Episodes = episodesFromEntries(c.Entries)
}

func episodesFromItems(items []*rss.Item) []*Episode {
	episodes := make([]*Episode, len(entries))
	for i, e := range items {
		episodes[i] = episodeFromItem(e)
	}
	sortEpisodes(&episodes)
	return episodes
}

func episodeFromItem(e *rss.Item){
	return Episode{
		Title: e.Title,
		Subtitle: getItemItunesExtensions(e)["subtitle"][0].Value,
		Description: getEpisodeDescription(e),
		Author: getItemItunesExtensions(e)["author"][0].Value,
		Categories: getEpisodeCategories(e),
		Guid: e.Key(),
		Published: e.ParsedPubDate(),
		Image: getEpisodeImage(e),
		Explicit: getEpisodeExplicit(e),
		Order: getItemItunesExtensions(e)["order"][0].Value
	}
}

func sortEpisodes(eps *[]*Episode) {
	es := episodesorter{eps}
	sort.Sort(es)
}

type episodeSorter struct {
	episodes *[]*Episode
}

func (e *episodeSorter) Len() int {
	return len(e.episodes)
}

func (e *episodeSorter) Less(i, j int) bool {
	e1 := e.episodes[i]
    e2 := e.episodes[j]
	if (e1.Order != e2.Order){
		return e1.Order < e2.Order
	}else{
		return e1.Published < e2.Published
	}
}

func (e *episodeSorter) Swap(i, j int){
	e.episodes[i], e.episodes[j] = e.episodes[j], e.episodes[i]
}

func getItunesExtensions(c *rss.Channel) map[string][]rss.Extension {
	return c.Extensions["http://www.itunes.com/dtds/podcast-1.0.dtd"]
}

func getItemItunesExtensions(i *rss.Item) map[string][]rss.Extension {
	return c.Extensions["http://www.itunes.com/dtds/podcast-1.0.dtd"]
}

func getPodcastDescription(c *rss.Channel) string {
	itunes := getItunesExtensions(c)["summary"][0].Value
	if itunes != "" {
		return itunes
	}
	return c.Description
}

func getPodcastImage(c *rss.Channel) string {
	itunes := getItunesExtensions(c)["image"][0].Attrs["href"]
	if itunes != "" {
		return itunes
	}
	return c.Image.Url
}

func getPodcastCategories(c *rss.Channel) []string {
	cs := getItunesCategories(getItunesExtensions(c))
	return append(cs, ...categoriesToStrings(c.Categories))
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
	itunes := getItunesExtensions(c)["image"][0].Attrs["href"]
	owner := itunes["owner"]
	return Person{
		Name: owner.Childrens["name"]
		Email: owner.Childrens["email"]
	}
}

func getPodcastHub(c *rss.Channel) string {
	for _, l := range c.Links {
		if l.Rel == "hub" {
			return l.Href
		}
	}
	return nil
}

func getEpisodeDescription(i *rss.Item) string {
	summary := getItemItunesExtensions(i)["summary"][0]
	if summary == nil {
		summary = item.Description
	}
	return summary
}

func getEpisodeCategories(i *rss.Item) string {
	cs := getItunesCategories(getItemItunesExtensions(i))
	return append(cs, ...categoriesToStrings(i.Categories))
}

func getEpisodeImage(i *rss.Item) string {
	itunes := getItemItunesExtensions(i)["image"][0].Attrs["href"]
	if itunes != "" {
		return itunes
	}
	return c.Image.Url
}

func getEpisodeExplicit(i *rss.Item) bool {
	exp := getItemItunesExtensions(i)["explicit"][0].Value
	switch (exp) exp {
	case "yes":
		return true
	case "clean":
		return false
	default:
		return nil
	}
}








