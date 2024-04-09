package httpserver

// ImageRequest is a request to upload an image into ml-service.
type ImageRequest struct {
	// Image is the binary image.
	Image []byte
	// IsBroker is flag that broker should be used.
	IsBroker bool
	// Hours is the number of hours in the image to check.
	Hours int
	// Hours is the number of minutes in the image to check.
	Minutes int
}

type ErrorResponse struct {
	Message string `json:"message"`
}

type SuccessResponse struct {
	Result int `json:"result"`
}
