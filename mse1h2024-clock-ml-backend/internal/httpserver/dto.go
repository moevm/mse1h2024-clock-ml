package httpserver

type ImageRequest struct {
	EncodedImage string       `json:"encoded_image" binding:"required"`
	Metadata     MetadataBase `json:"metadata" binding:"required"`
}

type MetadataBase struct {
	Width  int    `json:"width" binding:"required"`
	Height int    `json:"height" binding:"required"`
	Format string `json:"format" binding:"required"`
}
