package crawler

import (
    "fmt"
    "net/http"
	"time"

	"appengine"
	"appengine/datastore"
	"appengine/urlfetch"
	rss"github.com/jteeuwen/go-pkg-rss"
)

func init() {
    http.HandleFunc("/crawler/fetch", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	c := appengine.NewContext(r)
	feed := fetchFeed(r.Form.Get("url"), c)
    fmt.Fprintf(w, "%#f", feed)
}

type NoopHandler bool

func (i *NoopHandler) ProcessItems(f *rss.Feed, c *rss.Channel, itms []*rss.Item) {}
func (i *NoopHandler) ProcessChannels(f *rss.Feed, c []*rss.Channel) {}

func fetchFeed(url string, c appengine.Context) *rss.Feed {
    ni := new(NoopHandler)
	client := urlfetch.Client(c)
	feed := rss.NewWithHandlers(5, true, ni, ni)
	err := feed.FetchClient("http://feeds.twit.tv/sn.xml", client, nil)
	if err != nil {
		panic(err)
	}
	return 	feed
}
