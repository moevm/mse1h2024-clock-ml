package httpserver

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"time"

	"backend/internal/rabbitmq"

	"backend/internal/logger"
	"backend/internal/restapi"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

type Server struct {
	*http.Server
	log *logger.Logger
}

// Listen starts the server, waits for its graceful shutdown or context cancellation
func (s *Server) Listen(ctx context.Context) error {
	errChan := make(chan error)

	defer func() {
		close(errChan)
	}()

	go func() {
		errChan <- s.ListenAndServe()
	}()

	select {
	case <-ctx.Done():
		shutdownCtx, cancel := context.WithTimeout(
			context.Background(),
			5*time.Second,
		)
		defer cancel()

		if err := s.Shutdown(shutdownCtx); err != nil {
			s.log.Error("Error during server shutdown: %v\n", err)
		}

		return ctx.Err()
	case err := <-errChan:
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			return err
		}
		return nil
	}
}

// New creates a new Server instance.
func New(log *logger.Logger, rabbit rabbitmq.Publisher, rest restapi.Service, port int) *Server {
	router := chi.NewRouter()

	router.Use(log.LoggerMiddleware())
	router.Use(middleware.Recoverer)
	router.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"https://*", "http://*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Content-Type"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: false,
		MaxAge:           300,
	}))

	s := &Server{
		Server: &http.Server{
			Addr:    fmt.Sprintf(":%d", port),
			Handler: router,
		},
	}

	router.Route("/api/v1/", func(r chi.Router) {
		SetRoutes(r, rabbit, rest)
	})

	return s
}
