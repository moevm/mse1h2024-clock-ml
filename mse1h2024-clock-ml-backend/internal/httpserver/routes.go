package httpserver

import (
	"backend/internal/logger"
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"

	"github.com/go-chi/chi/v5"
)

// SetRoutes sets all server endpoints
func SetRoutes(
	router *chi.Mux,
	publisher publisher.RabbitmqPublisher,
	service restapi.Service,
	logger *logger.Logger,
) {
	handlers := NewHandlers(publisher, service, logger)

	router.Route("/process", func(apiRoute chi.Router) {
		apiRoute.Post("/sendPicture", handlers.SendPicture())
	})
}
