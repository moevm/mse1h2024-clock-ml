package logger

import (
	"context"
	"log/slog"
)

func Log(ctx context.Context, level slog.Level, format string, args ...interface{}) {
	log := ctx.Value(logKey).(*Logger)
	log.Log(ctx, level, format, args...)
}
