# import requirements
import torch
import cv2
import numpy as np
from torchvision import transforms, models


class Model:
    def __init__(self, weights_path : str = "./weights.pth") -> None:
        self.__model = models.resnet34()
        self.__device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        self.__model.load_state_dict(torch.load(weights_path, map_location=torch.device("cpu")))
        self.__evaluate_mode = False
        
        self.__mean_normalize = [0.485, 0.456, 0.406]
        self.__std_normalize = [0.229, 0.224, 0.225]
        
        self.__classes = [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    
    def predict_class(self, image: np.array) -> int:
        if not self.__evaluate_mode:
            self.__evaluate_mode = True
            self.__model.eval()
        
        input_tensor = self.get_image_tensor(image)
        input_tensor = input_tensor.to(self.__device)
        
        with torch.no_grad():
            output = self.__model(input_tensor).argmax(1)
        
        predicted_class = self.__classes[output]
        return predicted_class    
        
    def get_image_tensor(self, image: np.array):
        transform = transforms.Compose([
            transforms.Resize((144, 144)),
            transforms.ToTensor(),
            transforms.Normalize(self.__mean_normalize, self.__std_normalize)
        ])
        
        image = transforms.functional.to_pil_image(image)
        tensor = transform(image)
        tensor = tensor.unsqueeze(0)
        return tensor
        
        
if __name__ == '__main__':
    model = Model()
    
    image = cv2.imread("../processing/images/6balla_1.png")
    
    predicted = model.predict_class(image)
    print(f"Кол-во баллов = {predicted}")