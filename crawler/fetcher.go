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

func updatePodcasts(podcasts []*Podcast, c appengine.Context) {
	n := len(podcasts)
	progress := make(chan int, n)

	for i, p := range podcasts {
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
}

func createOrUpdatePodcastByUrl(url string, c appengine.Context) (*Podcast, error) {
	p := new(Podcast)
	p.Url = url

	key := datastore.NewKey(c, "Podcast", url, 0, nil)
	err := datastore.Get(c, key, p)
	if err != nil && err != datastore.ErrNoSuchEntity {
		return nil, err
	}

	updatePodcasts([]*Podcast{p}, c)

	_, err = datastore.Put(c, key, p)

	return p, err
}
