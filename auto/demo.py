from PicGen import StableDiffusion

obj = StableDiffusion(
    web_url = 'http://127.0.0.1:7860', 
    checkpoint = 'pastelMixStylizedAnime_pastelMixPrunedFP16.safetensors', 
    vae = 'kl-f8-anime2.ckpt')

print(obj.get_embeddings())
print(obj.get_models())
print(obj.get_loras())
print(obj.get_vaes())
print(obj.generate_imgs())