package crawler

import (
	"net/http"

	"appengine"
	"github.com/davecgh/go-spew/spew"
)

func init() {
	http.HandleFunc("/crawler/fetch", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	c := appengine.NewContext(r)
	podcast, err := createOrUpdatePodcastByUrl(r.Form.Get("url"), c)
	if err != nil {
		c.Errorf("%v", err)
		http.Error(w, err.Error(), 500)
		return
	}

	spew.Fdump(w, podcast)
	w.Write([]byte("done"))
}
