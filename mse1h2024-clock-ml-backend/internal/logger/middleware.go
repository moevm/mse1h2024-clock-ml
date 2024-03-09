package logger

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"time"
)

type contextKey string

const (
	logKey contextKey = "log"
)

type Logger struct {
	*slog.Logger
}

func New(level slog.Level) *Logger {
	return &Logger{
		Logger: slog.New(
			slog.NewTextHandler(
				os.Stdout,
				&slog.HandlerOptions{
					Level: level,
				},
			),
		),
	}
}

func(l *Logger) LoggerMiddleware() func(next http.Handler) http.Handler {
	l.Info("logger middleware enabled")

	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			defer func() {
				l.Info(
					"request handled",
					slog.String("path", r.URL.Path),
					slog.String("query", r.URL.RawQuery),
					slog.String("method", r.Method),
					slog.String("remote_addr", r.RemoteAddr),
					slog.String("duration", time.Since(start).String()),
				)
			}()

			ctx := r.Context()
			ctx = context.WithValue(ctx, logKey, l)
			r = r.WithContext(ctx)
			next.ServeHTTP(w, r)
		})
	}
}
