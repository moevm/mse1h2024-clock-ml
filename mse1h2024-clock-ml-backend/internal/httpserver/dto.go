package httpserver

// ImageRequest is a request to upload an image into ml-service.
type ImageRequest struct {
	// EncodedImage is the base64 encoded image.
	EncodedImage string `json:"encoded_image" binding:"required"`
	// Metadata is the metadata of the image.
	Metadata Metadata `json:"metadata" binding:"required"`
}

type Metadata struct {
	Width  int    `json:"width" binding:"required"`
	Height int    `json:"height" binding:"required"`
	Format string `json:"format" binding:"required"`
}

type ErrorResponse struct {
	Message string `json:"message"`
}
