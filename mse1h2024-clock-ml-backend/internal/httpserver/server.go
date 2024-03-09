package httpserver

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"time"

	"backend/internal/logger"
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
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

// NewServer creates a new Server instance.
func NewServer(
	log *logger.Logger,
	publisher publisher.RabbitmqPublisher,
	service restapi.Service,
	port int,
) *Server {
	router := chi.NewRouter()

	logMiddleware := log.LoggerMiddleware()

	router.Use(logMiddleware)
	router.Use(middleware.Recoverer)

	s := &Server{
		Server: &http.Server{
			Addr:    fmt.Sprintf(":%d", port),
			Handler: router,
		},
	}

	SetRoutes(router, publisher, service, log)

	return s
}
