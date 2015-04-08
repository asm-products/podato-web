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
	podcast := updatePodcastsByUrl([]string{r.Form.Get("url")}, c)[0]

	spew.Fdump(w, podcast)
	w.Write([]byte("done"))
}
