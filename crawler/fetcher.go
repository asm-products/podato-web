package crawler

import (
	"appengine"
	"appengine/datastore"
	"appengine/urlfetch"
	rss "github.com/jteeuwen/go-pkg-rss"
)

type NoopHandler bool

func (i *NoopHandler) ProcessItems(f *rss.Feed, c *rss.Channel, itms []*rss.Item) {}
func (i *NoopHandler) ProcessChannels(f *rss.Feed, c []*rss.Channel)              {}

func fetchFeed(url string, c appengine.Context) (*rss.Feed, error) {
	c.Infof("Fetching: %v", url)
	ni := new(NoopHandler)
	client := urlfetch.Client(c)
	feed := rss.NewWithHandlers(5, true, ni, ni)
	err := feed.FetchClient(url, client, nil)
	return feed, err
}

func updatePodcast(p *Podcast, c appengine.Context) error {
	f, err := fetchFeed(p.Url, c)
	if err != nil {
		return err
	}
	p.UpdateFromFeed(f)
	return err
}

func updatePodcasts(podcasts []*Podcast, c appengine.Context) appengine.MultiError {
	n := len(podcasts)
	progress := make(chan int, n)
	errors := make([]error, n)

	for i, p := range podcasts {
		go func() {
			errors[i] = updatePodcast(p, c)
			c.Infof("updated %v", i)
			progress <- i
		}()

	}

	for j := 0; j < n; j++ {
		c.Infof("done %v", <-progress)
	}

	return errors
}

func createOrUpdatePodcastByUrl(url string, c appengine.Context) (*Podcast, error) {
	p := new(Podcast)
	p.Url = url

	key := datastore.NewKey(c, "Podcast", url, 0, nil)
	err := datastore.Get(c, key, p)
	if err != nil && err != datastore.ErrNoSuchEntity {
		return nil, err
	}

	err = updatePodcasts([]*Podcast{p}, c)[0]
	if err != nil {
		return p, err
	}

	_, err = datastore.Put(c, key, p)

	return p, err
}
