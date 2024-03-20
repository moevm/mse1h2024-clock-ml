package httpserver

// ImageRequest is a request to upload an image into ml-service.
type ImageRequest struct {
	// EncodedImage is the base64 encoded image.
	EncodedImage string `json:"encoded_image" binding:"required"`
	// IsBroker is flag that broker should be used.
	IsBroker bool `json:"is_broker"`
	// Metadata is the metadata of the image.
	Metadata Metadata `json:"metadata"`
}

type Metadata struct {
	Width  int    `json:"width"`
	Height int    `json:"height"`
	Format string `json:"format"`
}

type ErrorResponse struct {
	Message string `json:"message"`
}

type SuccessResponse struct {
	Result int `json:"result"`
}
