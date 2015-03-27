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
	Explicit int8 `datastore:"explicit"`
	Likes int32 `datastore:"likes,noindex"`
	Dislikes int32 `datastore:"dislikes,noindex"`
	Views int32 `datastore:"views"`
	Order int `datastore:"-"`
}



