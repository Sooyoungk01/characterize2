# My code here ... lets rock it ... yeahhhhh..

# %load_ext autoreload
# %autoreload 2

import os

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
os.chdir('../')
CODE_DIR = '/content/DualStyleGAN'
device = 'cuda'

os.chdir(f'/content/DualStyleGAN')
MODEL_DIR = os.path.join(os.path.dirname(os.getcwd()), CODE_DIR, 'checkpoint')
DATA_DIR = os.path.join(os.path.dirname(os.getcwd()), CODE_DIR, 'data')

import sys

sys.path.append(".")
sys.path.append("..")

import numpy as np
import torch
from util import save_image, load_image, visualize
import argparse
from argparse import Namespace
from torchvision import transforms
from torch.nn import functional as F
import torchvision
import matplotlib.pyplot as plt
from model.dualstylegan import DualStyleGAN
from model.sampler.icp import ICPTrainer
from model.encoder.psp import pSp

style_types = ['cartoon', 'caricature', 'anime', 'arcane', 'comic', 'pixar', 'slamdunk']
style_type = style_types[0]

if not os.path.exists(os.path.join(MODEL_DIR, style_type)):
    os.makedirs(os.path.join(MODEL_DIR, style_type))


def get_download_model_command(file_id, file_name):
    """ Get wget download command for downloading the desired model and save to directory ../checkpoint/. """
    current_directory = os.getcwd()
    save_path = MODEL_DIR
    url = r"""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={FILE_ID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={FILE_ID}" -O {SAVE_PATH}/{FILE_NAME} && rm -rf /tmp/cookies.txt""".format(
        FILE_ID=file_id, FILE_NAME=file_name, SAVE_PATH=save_path)
    return url


MODEL_PATHS = {
    "encoder": {"id": "1NgI4mPkboYvYw3MWcdUaQhkr0OWgs9ej", "name": "encoder.pt"},
    "cartoon-G": {"id": "1exS9cSFkg8J4keKPmq2zYQYfJYC5FkwL", "name": "generator.pt"},
    "cartoon-N": {"id": "1JSCdO0hx8Z5mi5Q5hI9HMFhLQKykFX5N", "name": "sampler.pt"},
    "cartoon-S": {"id": "1ce9v69JyW_Dtf7NhbOkfpH77bS_RK0vB", "name": "refined_exstyle_code.npy"},
    "caricature-G": {"id": "1BXfTiMlvow7LR7w8w0cNfqIl-q2z0Hgc", "name": "generator.pt"},
    "caricature-N": {"id": "1eJSoaGD7X0VbHS47YLehZayhWDSZ4L2Q", "name": "sampler.pt"},
    "caricature-S": {"id": "1-p1FMRzP_msqkjndRK_0JasTdwQKDsov", "name": "refined_exstyle_code.npy"},
    "anime-G": {"id": "1BToWH-9kEZIx2r5yFkbjoMw0642usI6y", "name": "generator.pt"},
    "anime-N": {"id": "19rLqx_s_SUdiROGnF_C6_uOiINiNZ7g2", "name": "sampler.pt"},
    "anime-S": {"id": "17-f7KtrgaQcnZysAftPogeBwz5nOWYuM", "name": "refined_exstyle_code.npy"},
    "arcane-G": {"id": "15l2O7NOUAKXikZ96XpD-4khtbRtEAg-Q", "name": "generator.pt"},
    "arcane-N": {"id": "1fa7p9ZtzV8wcasPqCYWMVFpb4BatwQHg", "name": "sampler.pt"},
    "arcane-S": {"id": "1z3Nfbir5rN4CrzatfcgQ8u-x4V44QCn1", "name": "exstyle_code.npy"},
    "comic-G": {"id": "1_t8lf9lTJLnLXrzhm7kPTSuNDdiZnyqE", "name": "generator.pt"},
    "comic-N": {"id": "1RXrJPodIn7lCzdb5BFc03kKqHEazaJ-S", "name": "sampler.pt"},
    "comic-S": {"id": "1ZfQ5quFqijvK3hO6f-YDYJMqd-UuQtU-", "name": "exstyle_code.npy"},
    "pixar-G": {"id": "1TgH7WojxiJXQfnCroSRYc7BgxvYH9i81", "name": "generator.pt"},
    "pixar-N": {"id": "18e5AoQ8js4iuck7VgI3hM_caCX5lXlH_", "name": "sampler.pt"},
    "pixar-S": {"id": "1I9mRTX2QnadSDDJIYM_ntyLrXjZoN7L-", "name": "exstyle_code.npy"},
    "slamdunk-G": {"id": "1MGGxSCtyf9399squ3l8bl0hXkf5YWYNz", "name": "generator.pt"},
    "slamdunk-N": {"id": "1-_L7YVb48sLr_kPpOcn4dUq7Cv08WQuG", "name": "sampler.pt"},
    "slamdunk-S": {"id": "1Dgh11ZeXS2XIV2eJZAExWMjogxi_m_C8", "name": "exstyle_code.npy"},
}

# download pSp encoder
path = MODEL_PATHS["encoder"]
download_command = get_download_model_command(file_id=path["id"], file_name=path["name"])
# print(download_command)
os.system(f"{download_command}")
# !{download_command}

# download dualstylegan
path = MODEL_PATHS[style_type + '-G']
download_command = get_download_model_command(file_id=path["id"], file_name=os.path.join(style_type, path["name"]))
os.system(f"{download_command}")
# !{download_command}
# download sampler
path = MODEL_PATHS[style_type + '-N']
download_command = get_download_model_command(file_id=path["id"], file_name=os.path.join(style_type, path["name"]))
# !{download_command}
os.system(f"{download_command}")
# download extrinsic style code
path = MODEL_PATHS[style_type + '-S']
download_command = get_download_model_command(file_id=path["id"], file_name=os.path.join(style_type, path["name"]))
# !{download_command}
os.system(f"{download_command}")

transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(256),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)

# load DualStyleGAN
generator = DualStyleGAN(1024, 512, 8, 2, res_index=6)
generator.eval()
ckpt = torch.load(os.path.join(MODEL_DIR, style_type, 'generator.pt'), map_location=lambda storage, loc: storage)
generator.load_state_dict(ckpt["g_ema"])
generator = generator.to(device)

# load encoder
model_path = os.path.join(MODEL_DIR, 'encoder.pt')
ckpt = torch.load(model_path, map_location='cpu')
opts = ckpt['opts']
opts['checkpoint_path'] = model_path
opts = Namespace(**opts)
opts.device = device
encoder = pSp(opts)
encoder.eval()
encoder = encoder.to(device)

# load extrinsic style code
exstyles = np.load(os.path.join(MODEL_DIR, style_type, MODEL_PATHS[style_type + '-S']["name"]),
                   allow_pickle='TRUE').item()

# load sampler network
icptc = ICPTrainer(np.empty([0, 512 * 11]), 128)
icpts = ICPTrainer(np.empty([0, 512 * 7]), 128)
ckpt = torch.load(os.path.join(MODEL_DIR, style_type, 'sampler.pt'), map_location=lambda storage, loc: storage)
icptc.icp.netT.load_state_dict(ckpt['color'])
icpts.icp.netT.load_state_dict(ckpt['structure'])
icptc.icp.netT = icptc.icp.netT.to(device)
icpts.icp.netT = icpts.icp.netT.to(device)

print('Model successfully loaded!')

##### Step 5: Visualize Input


image_path = './data/content/unsplash-rDEOVtE7vOs.jpg'
# image_path = '/content/hhh.jpg'
original_image = load_image(image_path)

plt.figure(figsize=(10, 10), dpi=30)
visualize(original_image[0])
plt.show()

# Align Image
if_align_face = True


def run_alignment(image_path):
    import dlib
    from model.encoder.align_all_parallel import align_face
    modelname = os.path.join(MODEL_DIR, 'shape_predictor_68_face_landmarks.dat')
    if not os.path.exists(modelname):
        import wget, bz2
        wget.download('http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2', modelname + '.bz2')
        zipfile = bz2.BZ2File(modelname + '.bz2')
        data = zipfile.read()
        open(modelname, 'wb').write(data)
    predictor = dlib.shape_predictor(modelname)
    aligned_image = align_face(filepath=image_path, predictor=predictor)
    return aligned_image


if if_align_face:
    I = transform(run_alignment(image_path)).unsqueeze(dim=0).to(device)
else:
    I = F.adaptive_avg_pool2d(load_image(image_path).to(device), 256)

plt.figure(figsize=(10, 10), dpi=30)
visualize(I[0].cpu())
plt.show()

style_id = 26

# try to load the style image
stylename = list(exstyles.keys())[style_id]
stylepath = os.path.join(DATA_DIR, style_type, 'images/train', stylename)
print('loading %s' % stylepath)
if os.path.exists(stylepath):
    S = load_image(stylepath)
    plt.figure(figsize=(10, 10), dpi=30)
    visualize(S[0])
    plt.show()
else:
    print('%s is not found' % stylename)

with torch.no_grad():
    img_rec, instyle = encoder(I, randomize_noise=False, return_latents=True,
                               z_plus_latent=True, return_z_plus_latent=True, resize=False)
    img_rec = torch.clamp(img_rec.detach(), -1, 1)

    latent = torch.tensor(exstyles[stylename]).repeat(2, 1, 1).to(device)
    # latent[0] for both color and structrue transfer and latent[1] for only structrue transfer
    latent[1, 7:18] = instyle[0, 7:18]
    exstyle = generator.generator.style(latent.reshape(latent.shape[0] * latent.shape[1], latent.shape[2])).reshape(
        latent.shape)

    img_gen, _ = generator([instyle.repeat(2, 1, 1)], exstyle, z_plus_latent=True,
                           truncation=0.7, truncation_latent=0, use_res=True, interp_weights=[0.6] * 7 + [1] * 11)
    img_gen = torch.clamp(img_gen.detach(), -1, 1)
    # deactivate color-related layers by setting w_c = 0
    img_gen2, _ = generator([instyle], exstyle[0:1], z_plus_latent=True,
                            truncation=0.7, truncation_latent=0, use_res=True, interp_weights=[0.6] * 7 + [0] * 11)
    img_gen2 = torch.clamp(img_gen2.detach(), -1, 1)

# Visualize Results

vis = torchvision.utils.make_grid(F.adaptive_avg_pool2d(torch.cat([img_rec, img_gen, img_gen2], dim=0), 256), 4, 1)
plt.figure(figsize=(10, 10), dpi=120)
visualize(vis.cpu())
plt.show()

results = []
# for i in range(6): # change weights of structure codes
#     for j in range(6): # change weights of color codes
#         w = [i/5.0]*7+[j/5.0]*11

#         img_gen, _ = generator([instyle], exstyle[0:1], z_plus_latent=True,
#                                 truncation=0.7, truncation_latent=0, use_res=True, interp_weights=w)
#         img_gen = torch.clamp(F.adaptive_avg_pool2d(img_gen.detach(), 128), -1, 1)
#         results += [img_gen]

w = [5 / 5.0] * 7 + [5 / 5.0] * 11

img_gen, _ = generator([instyle], exstyle[0:1], z_plus_latent=True,
                       truncation=0.7, truncation_latent=0, use_res=True, interp_weights=w)
img_gen = torch.clamp(F.adaptive_avg_pool2d(img_gen.detach(), 128), -1, 1)
results += [img_gen]

from torchvision.utils import save_image

vis = torchvision.utils.make_grid(torch.cat(results, dim=0), 6, 1)
# vis = torchvision.utils.make_grid(torch.cat(results, dim=0), 6, 1)
# print("image is: ", vis)
# ff = vis.cpu()
# ff = ff.numpy()
# ff.save('savedimage.png', dpi=120)
save_image(results[0], '/content/img1.jpg')
plt.figure(figsize=(10, 10), dpi=120)
visualize(vis.cpu())
plt.show()
