package httpserver

import (
	"backend/internal/rabbitmq"
	"backend/internal/restapi"
	"net/http"

	"github.com/go-chi/chi/v5"
)

// SetRoutes sets up all server endpoints.
func SetRoutes(r chi.Router, rabbit rabbitmq.Publisher, rest restapi.Service) {
	r.Post("/process", SendPicture(rabbit, rest))

	r.Get("/ping", func(w http.ResponseWriter, r *http.Request) {
		_, _ = w.Write([]byte("pong"))
	})
}
