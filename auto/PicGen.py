import random
import requests
import io
import base64
from PIL import Image
import random

class StableDiffusion:
    # AUTOMATIC1111 web-ui v1.6
    # use loras and embeddings in (negative)prompt
    # more api see "http://127.0.0.1:7860/docs", pay special attention to "option" api
    def __init__(self, web_url = None, checkpoint = None, vae = None, prompt = None, negative_prompt = None, payload = None):
        self._web_url = web_url if web_url else "http://127.0.0.1:7860"
        self._checkpoint = checkpoint if checkpoint else "sd-v1-4.ckpt"
        self._vae = vae if vae else "vae-ft-mse-840000-ema-pruned.safetensors"
        self._prompt = prompt if prompt else "masterpiece, best quality, ultra-detailed, illustration, portrait, 1girl"
        self._negative_prompt = negative_prompt if negative_prompt else "lowres, ((bad anatomy)), ((bad hands)), text, missing finger, extra digits, fewer digits, blurry, ((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), (ugly), ((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), ((extra feet)), monster, logo, cropped, worst quality, low quality, normal quality, jpeg, humpbacked, long body, long neck, ((jpeg artifacts)), hands up"
        
        if payload:
            self._payload = payload
        else:
            self._payload = {
                "enable_hr": True,
                "hr_scale": 2,
                "width": 640,
                "height": 360,

                "denoising_strength": 0.6,
                "hr_upscaler": "Latent",
                "hr_second_pass_steps": 20,
                
                "sampler_name": "DPM++ 2M Karras",
                "steps": 20,
                "cfg_scale": 7
            }
            

    def generate_imgs(self):
        # stable diffusion
        self._payload["prompt"] = self._prompt
        self._payload["negative_prompt"] = self._negative_prompt
        
        self._payload["override_settings"] = {
            "sd_model_checkpoint": self._checkpoint,
            "sd_vae": self._vae,
            "CLIP_stop_at_last_layers": 2
        }

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
    
    def get_models(self):
        requests.post(url=f'{self._web_url}/sdapi/v1/refresh-checkpoints')
        r = requests.get(url=f'{self._web_url}/sdapi/v1/sd-models').json()
        return [item["model_name"] for item in r]
        
    def get_loras(self):
        requests.post(url=f'{self._web_url}/sdapi/v1/refresh-loras')
        r = requests.get(url=f'{self._web_url}/sdapi/v1/loras').json()
        return [item["name"] for item in r]
    
    def get_vaes(self):
        requests.post(url=f'{self._web_url}/sdapi/v1/refresh-vae')
        r = requests.get(url=f'{self._web_url}/sdapi/v1/sd-vae').json()
        return [item["model_name"] for item in r]

    def get_embeddings(self):
        r = requests.get(url=f'{self._web_url}/sdapi/v1/embeddings').json()
        return {key: list(r[key].keys()) for key in r}
    
    #region setter&getter
    @property
    def web_url(self):
        return self._web_url

    @web_url.setter
    def web_url(self, value):
        self._web_url = value
    
    @property
    def checkpoint(self):
        return self._checkpoint

    @checkpoint.setter
    def checkpoint(self, value):
        self._checkpoint = value
    
    @property
    def vae(self):
        return self._vae

    @vae.setter
    def vae(self, value):
        self._vae = value

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value
    
    @property
    def negative_prompt(self):
        return self._negative_prompt

    @negative_prompt.setter
    def negative_prompt(self, value):
        self._negative_prompt = value
    
    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value
    #endregion setter&getter