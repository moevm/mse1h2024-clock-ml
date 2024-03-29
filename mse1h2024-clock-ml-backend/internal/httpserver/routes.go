package httpserver

import (
	"net/http"
	
	"backend/internal/rabbitmq"
	"backend/internal/restapi"

	"github.com/go-chi/chi/v5"
)

// SetRoutes sets up all server endpoints.
func SetRoutes(r chi.Router, rabbit rabbitmq.Publisher, rest restapi.Service) {
	r.Post("/get-estimation", SendPicture(rabbit, rest))

	r.Get("/ping", func(w http.ResponseWriter, r *http.Request) {
		_, _ = w.Write([]byte("pong"))
	})
}
