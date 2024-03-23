package httpserver

// ImageRequest is a request to upload an image into ml-service.
type ImageRequest struct {
	// Image is the binary image.
	Image []byte
	// IsBroker is flag that broker should be used.
	IsBroker bool
}

type ErrorResponse struct {
	Message string `json:"message"`
}

type SuccessResponse struct {
	Result int `json:"result"`
}
