package crawler

import (
	"appengine"
	"appengine/datastore"
	"appengine/urlfetch"
	"github.com/davecgh/go-spew/spew"
	rss "github.com/jteeuwen/go-pkg-rss"
)

type NoopHandler bool

func (i *NoopHandler) ProcessItems(f *rss.Feed, c *rss.Channel, itms []*rss.Item) {}
func (i *NoopHandler) ProcessChannels(f *rss.Feed, c []*rss.Channel)              {}

func fetchFeed(url string, c appengine.Context) *rss.Feed {
	c.Infof("Fetching: %v", url)
	ni := new(NoopHandler)
	client := urlfetch.Client(c)
	feed := rss.NewWithHandlers(5, true, ni, ni)
	err := feed.FetchClient(url, client, nil)
	if err != nil {
		panic(err)
	}
	return feed
}

func updatePodcast(p *Podcast, c appengine.Context) {
	f := fetchFeed(p.Url, c)
	p.UpdateFromFeed(f)
}

func updatePodcastsByUrl(urls []string, c appengine.Context) []*Podcast {
	n := len(urls)
	keys := make([]*datastore.Key, n)
	podcasts := make([]*Podcast, n)
	progress := make(chan int, n)

	for i, url := range urls {
		keys[i] = datastore.NewKey(c, "Podcast", url, 0, nil)
		podcasts[i] = new(Podcast)
	}

	datastore.GetMulti(c, keys, podcasts)

	for i, p := range podcasts {
		if p == nil {
			*p = Podcast{}
		}
		if p.Url == "" {
			p.Url = urls[i]
		}
		go func() {
			updatePodcast(p, c)
			c.Infof("updated %v", i)
			progress <- i
			c.Infof("%v", spew.Sdump(p))
		}()

	}

	for j := 0; j < n; j++ {
		c.Infof("done %v", <-progress)
	}

	_, err := datastore.PutMulti(c, keys, podcasts)

	if err != nil {
		c.Errorf("%v", err)
	}

	return podcasts
}
