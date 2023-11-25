import random
import requests
import io
import base64
from PIL import Image
import random

class StableDiffusion:
    
    def __init__(self, web_url="http://127.0.0.1:7860", payload=None):
        self._web_url = web_url
        
        if payload is None:
            self._payload = {
                "enable_hr": True,
                "denoising_strength": 0.6,
                "hr_scale": 2,
                "hr_upscaler": "Latent",
                "hr_second_pass_steps": 20,
                "prompt": "masterpiece, best quality, ultra-detailed, illustration, portrait, 1girl",     #  提示词
                "seed": 4285880275,
                "sampler_name": "DPM++ 2M Karras",
                "steps": 20,
                "cfg_scale": 7,
                "width": 640,
                "height": 360,
                "negative_prompt": "lowres, ((bad anatomy)), ((bad hands)), text, missing finger, extra digits, fewer digits, blurry, ((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), (ugly), ((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), ((extra feet)), monster, logo, cropped, worst quality, low quality, normal quality, jpeg, humpbacked, long body, long neck, ((jpeg artifacts)), hands up",     #  负面提示词
            }
        else:
            self._payload = payload

    def generate_imgs(self):
        # stable diffusion
        # 生成一个范围在0到1000000之间的随机整数
        random_int = random.randint(0, 10**10)
        self._payload["seed"] = random_int
        response = requests.post(url=f'{self._web_url}/sdapi/v1/txt2img', json=self._payload)
        r = response.json()

        ans = []
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            ans.append(image)
        
        return ans
    
    @property
    def web_url(self):
        return self._web_url

    @web_url.setter
    def web_url(self, value):
        self._web_url = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value