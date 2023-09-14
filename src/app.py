import json
import logging
from typing import List

import numpy as np
from fastapi import Body, FastAPI, HTTPException, Response
from pydantic import BaseModel
from pymilvus import Collection, connections, utility

MILVUS_ALIAS = "default"
MILVUS_HOST = "localhost"
MILVUS_HOST_PORT = "9091"
MILVUS_COLLECTION = "job_description_emb"
MILVUS_ALIAS_NAME = "default"

connections.connect(alias=MILVUS_ALIAS_NAME)


search_params = {"metric_type": "L2", "params": {"nprobe": 84}, "offset": 0}

collection = Collection(MILVUS_COLLECTION)


app = FastAPI(docs_url="/swagger")


class SearchDataInput(BaseModel):
    embeddings: List[List[float]] = Body(...)

    class Config:
        schema_extra = {
            "example": {
                "embeddings": [
    [  -1.26276970e-01, -1.63079605e-01, -2.08067223e-02, -1.56895127e-02,
       -2.74752408e-01,  1.35791972e-01, -1.64737731e-01, -3.23561206e-03,
       -2.57613182e-01,  1.75985068e-01, -9.92538929e-02, -4.21305060e-01,
       -3.99871230e-01,  1.11615427e-01,  4.02423702e-02, -1.23877376e-02,
        4.62358564e-01,  1.16508976e-02,  3.88170063e-01, -1.15837097e-01,
       -2.44739026e-01,  7.93277249e-02, -3.27260703e-01, -1.32084116e-01,
       -4.82246488e-01,  2.83075608e-02, -1.15555584e-01, -4.72503722e-01,
        6.52014673e-01,  3.03771496e-01,  3.25455964e-01,  1.64139748e-01,
        7.06753969e-01, -2.94508368e-01, -4.02879447e-01,  8.36653113e-02,
        1.52506843e-01,  6.41081035e-02, -1.61431253e-01, -2.52058983e-01,
       -2.07937822e-01,  4.11202252e-01,  3.15080844e-02,  1.20159350e-01,
       -2.29835913e-01, -4.53162342e-02, -4.05692756e-01,  1.33937344e-01,
       -1.35376707e-01,  5.11769876e-02, -4.71586883e-01, -3.52770090e-01,
        2.01937780e-01, -3.15221369e-01, -1.50731817e-01, -3.29227924e-01,
        1.87779553e-02,  1.91294119e-01,  6.77901283e-02, -1.06891155e-01,
       -3.90466720e-01, -1.65440843e-01, -1.57209560e-02, -1.34941414e-01,
        2.49856878e-02,  2.04248935e-01, -3.44248340e-02, -3.51449251e-01,
        2.17993751e-01, -6.78116977e-02,  1.17265604e-01,  1.83369741e-01,
        9.52582136e-02, -1.84391260e-01,  1.49522394e-01,  6.07593179e-01,
        2.72362828e-01, -2.07094520e-01,  3.76562059e-01,  5.39476536e-02,
       -2.40647808e-01,  1.71261132e-02, -4.31767814e-02,  3.20920534e-02,
        1.48103371e-01,  3.16221446e-01, -4.29954648e-01,  2.09217325e-01,
       -3.87267709e-01, -1.64003253e-01, -2.01131165e-01, -3.07262003e-01,
       -2.86440551e-02, -1.22892290e-01,  3.18337590e-01,  4.01439458e-01,
        7.51925260e-02, -9.21263732e-03,  5.00396565e-02, -3.05492222e-01,
       -7.58155286e-02, -4.14243728e-01, -2.00496525e-01, -2.50973403e-01,
       -2.61921436e-01, -1.13164954e-01,  3.33427668e-01, -7.56839104e-03,
        2.38488153e-01,  4.02303003e-02, -2.58933216e-01, -1.32324453e-03,
       -2.06263781e-01, -3.11811358e-01, -2.66350776e-01, -1.74235716e-01,
       -5.61682209e-02, -6.63328171e-02,  4.17971313e-01,  1.52613088e-01,
        4.60087731e-02, -1.79366708e-01, -1.71570107e-02, -3.36123705e-01,
       -5.96168824e-03, -9.49413925e-02,  4.18247618e-02,  4.89979461e-02,
       -2.05092967e-01,  3.08273405e-01, -1.32361025e-01,  4.33506817e-03,
       -4.47878800e-02, -1.51306354e-02,  2.24833623e-01,  8.31025988e-02,
       -1.85253054e-01,  1.39592707e-01, -5.37444316e-02,  4.60581705e-02,
       -1.94257155e-01, -1.35470808e-01,  6.75847828e-02, -2.19107538e-01,
       -2.45748341e-01, -2.00621575e-01, -1.87920451e-01,  3.72733980e-01,
        2.39899196e-02, -2.05460578e-01,  2.74004459e-01,  2.84553990e-02,
        2.97413141e-01,  6.06363833e-01,  3.98686349e-01,  2.74770260e-01,
        2.74687082e-01, -8.29050541e-02, -2.19688386e-01,  6.20301217e-02,
       -1.42873719e-01, -1.22238219e-01,  1.01173520e-01,  2.55691595e-02,
       -1.03807546e-01, -1.12825811e-01, -2.76536018e-01, -2.97092319e-01,
       -2.94406474e-01,  1.10723339e-02, -5.34237385e-01, -3.67096290e-02,
       -9.67132673e-03, -1.67504624e-01, -1.58008978e-01, -2.39680618e-01,
        8.63035619e-02,  1.96732923e-01, -2.39867374e-01,  1.76191032e-02,
        1.94660947e-02, -3.50507259e-01,  9.82546881e-02, -6.53978214e-02,
       -6.43791929e-02,  4.53333199e-01, -6.74494356e-02,  2.05725431e-01,
        2.48260736e-01, -7.96512291e-02, -5.09492718e-02, -1.25820830e-01,
       -2.54160523e-01, -3.79837900e-01,  2.80270666e-01, -3.11355531e-01,
        1.00218251e-01, -2.05609590e-01,  2.66070187e-01,  8.94064456e-02,
       -1.07371770e-02,  2.40043029e-01, -3.06421995e-01,  1.17282093e-01,
        3.43994856e-01,  4.15822655e-01,  3.53698075e-01, -1.66001134e-02,
        1.70777529e-01,  2.12122381e-01,  3.01528424e-01,  2.12741643e-01,
       -5.18686846e-02, -3.47433031e-01, -6.92527741e-02,  3.57651487e-02,
       -3.31603646e-01, -3.69263813e-04, -1.68300420e-01,  1.93854436e-01,
       -6.24747396e-01,  1.61039904e-01,  8.47394615e-02,  2.06767067e-01,
        4.66150790e-02, -7.44918957e-02, -3.45102772e-02, -3.20701659e-01,
       -3.42431366e-01, -5.86029142e-02,  6.83633164e-02, -1.02490783e-01,
        6.36696041e-01,  1.32570788e-01,  1.58690363e-01,  3.81294265e-02,
       -5.66475019e-02,  6.83784112e-02, -4.77102280e-01, -1.03913136e-01,
        8.89730901e-02, -2.87425101e-01,  5.73363453e-02,  1.15170069e-01,
        1.89466134e-01,  6.39624596e-01, -8.51168483e-02, -3.60581815e-01,
       -1.81596681e-01, -2.13025436e-01, -4.08005752e-02,  4.65302579e-02,
        3.41815859e-01, -1.99242339e-01,  7.80186802e-02, -5.27780056e-01,
        2.82428525e-02,  1.70625314e-01,  3.02529037e-01, -4.11704779e-01,
        4.66627598e-01, -1.83744505e-01, -3.16921324e-02,  1.53818876e-01,
        4.90186781e-01,  2.14054421e-01, -1.60516083e-01,  7.45202303e-02,
        1.21610574e-01, -4.61614281e-02, -1.17486995e-02,  6.94388300e-02,
       -4.38876003e-02, -9.56380665e-02, -2.32885092e-01, -1.20004788e-01,
        1.78852260e-01,  1.93957791e-01, -3.25115919e-01,  4.77839857e-01,
        4.58942592e-01, -3.27724904e-01, -8.89120027e-02, -2.04065740e-02,
        2.04788655e-01, -2.69905508e-01,  5.66360801e-02,  4.83344868e-02,
       -9.87714082e-02,  2.36721411e-01, -3.72040048e-02,  2.03286022e-01,
        1.66709945e-02, -1.66082636e-01, -9.37711298e-02, -2.21098423e-01,
       -3.18903625e-02, -4.37021047e-01,  4.80386466e-02,  2.52574652e-01,
       -1.64837211e-01, -8.02500471e-02, -4.20770533e-02,  1.04366593e-01,
        7.25300610e-02, -2.12213725e-01,  1.78134337e-01,  2.10470125e-01,
        2.63405830e-01,  4.94371802e-02,  3.62759531e-01, -2.30380595e-01,
       -1.23702139e-01,  1.24911368e-01, -3.81581336e-01,  2.54870623e-01,
       -5.17856516e-03,  2.62863874e-01, -1.30387306e-01,  3.96716535e-01,
       -2.57542849e-01, -2.61414707e-01, -1.46659076e-01, -9.41694155e-02,
        3.98602307e-01, -3.37940693e-01, -7.92656362e-01, -2.23826364e-01,
       -3.22030425e-01,  3.87343913e-01, -2.41344765e-01, -1.09332621e-01,
       -5.45409203e-01, -3.60266924e-01,  3.70554656e-01,  2.65655071e-02,
       -2.53719985e-01,  4.41201538e-01, -3.97166491e-01,  8.13926682e-02,
       -1.01662669e-02,  9.75128412e-02,  3.28637183e-01,  1.94734722e-01,
       -9.46725011e-02, -1.92454487e-01,  3.29065114e-01,  2.31926084e-01,
        1.21656626e-01,  1.49020731e-01, -1.11507259e-01,  4.57766056e-01,
        2.81187836e-02, -2.48286948e-01, -1.87451795e-01,  2.67582357e-01,
        2.88918585e-01,  2.07469344e-01, -1.17748998e-01,  4.77143943e-01,
        7.09503964e-02,  4.33439016e-01, -2.51477063e-01,  1.71425074e-01,
        2.01444283e-01,  1.83082804e-01, -4.22960036e-02,  1.55468866e-01,
        2.57947482e-02, -2.85221517e-01, -4.18466568e-01,  4.66218889e-02,
       -2.63243794e-01,  3.96159858e-01,  3.41973603e-01,  2.39643931e-01,
        3.57474416e-01, -2.82690585e-01,  3.01905237e-02,  4.08621609e-01,
        8.58267173e-02,  3.27701747e-01,  2.60130912e-01,  3.79459083e-01]
                ]
            }
        }


class InsertDataInput(BaseModel):
    embeddings: List[List[float]] = Body(...)
    job_ids: List[str] = Body(...)

    class Config:
        schema_extra = {
            "example": {
                "embeddings": [
      [-1.26276970e-01, -1.63079605e-01, -2.08067223e-02, -1.56895127e-02,
       -2.74752408e-01,  1.35791972e-01, -1.64737731e-01, -3.23561206e-03,
       -2.57613182e-01,  1.75985068e-01, -9.92538929e-02, -4.21305060e-01,
       -3.99871230e-01,  1.11615427e-01,  4.02423702e-02, -1.23877376e-02,
        4.62358564e-01,  1.16508976e-02,  3.88170063e-01, -1.15837097e-01,
       -2.44739026e-01,  7.93277249e-02, -3.27260703e-01, -1.32084116e-01,
       -4.82246488e-01,  2.83075608e-02, -1.15555584e-01, -4.72503722e-01,
        6.52014673e-01,  3.03771496e-01,  3.25455964e-01,  1.64139748e-01,
        7.06753969e-01, -2.94508368e-01, -4.02879447e-01,  8.36653113e-02,
        1.52506843e-01,  6.41081035e-02, -1.61431253e-01, -2.52058983e-01,
       -2.07937822e-01,  4.11202252e-01,  3.15080844e-02,  1.20159350e-01,
       -2.29835913e-01, -4.53162342e-02, -4.05692756e-01,  1.33937344e-01,
       -1.35376707e-01,  5.11769876e-02, -4.71586883e-01, -3.52770090e-01,
        2.01937780e-01, -3.15221369e-01, -1.50731817e-01, -3.29227924e-01,
        1.87779553e-02,  1.91294119e-01,  6.77901283e-02, -1.06891155e-01,
       -3.90466720e-01, -1.65440843e-01, -1.57209560e-02, -1.34941414e-01,
        2.49856878e-02,  2.04248935e-01, -3.44248340e-02, -3.51449251e-01,
        2.17993751e-01, -6.78116977e-02,  1.17265604e-01,  1.83369741e-01,
        9.52582136e-02, -1.84391260e-01,  1.49522394e-01,  6.07593179e-01,
        2.72362828e-01, -2.07094520e-01,  3.76562059e-01,  5.39476536e-02,
       -2.40647808e-01,  1.71261132e-02, -4.31767814e-02,  3.20920534e-02,
        1.48103371e-01,  3.16221446e-01, -4.29954648e-01,  2.09217325e-01,
       -3.87267709e-01, -1.64003253e-01, -2.01131165e-01, -3.07262003e-01,
       -2.86440551e-02, -1.22892290e-01,  3.18337590e-01,  4.01439458e-01,
        7.51925260e-02, -9.21263732e-03,  5.00396565e-02, -3.05492222e-01,
       -7.58155286e-02, -4.14243728e-01, -2.00496525e-01, -2.50973403e-01,
       -2.61921436e-01, -1.13164954e-01,  3.33427668e-01, -7.56839104e-03,
        2.38488153e-01,  4.02303003e-02, -2.58933216e-01, -1.32324453e-03,
       -2.06263781e-01, -3.11811358e-01, -2.66350776e-01, -1.74235716e-01,
       -5.61682209e-02, -6.63328171e-02,  4.17971313e-01,  1.52613088e-01,
        4.60087731e-02, -1.79366708e-01, -1.71570107e-02, -3.36123705e-01,
       -5.96168824e-03, -9.49413925e-02,  4.18247618e-02,  4.89979461e-02,
       -2.05092967e-01,  3.08273405e-01, -1.32361025e-01,  4.33506817e-03,
       -4.47878800e-02, -1.51306354e-02,  2.24833623e-01,  8.31025988e-02,
       -1.85253054e-01,  1.39592707e-01, -5.37444316e-02,  4.60581705e-02,
       -1.94257155e-01, -1.35470808e-01,  6.75847828e-02, -2.19107538e-01,
       -2.45748341e-01, -2.00621575e-01, -1.87920451e-01,  3.72733980e-01,
        2.39899196e-02, -2.05460578e-01,  2.74004459e-01,  2.84553990e-02,
        2.97413141e-01,  6.06363833e-01,  3.98686349e-01,  2.74770260e-01,
        2.74687082e-01, -8.29050541e-02, -2.19688386e-01,  6.20301217e-02,
       -1.42873719e-01, -1.22238219e-01,  1.01173520e-01,  2.55691595e-02,
       -1.03807546e-01, -1.12825811e-01, -2.76536018e-01, -2.97092319e-01,
       -2.94406474e-01,  1.10723339e-02, -5.34237385e-01, -3.67096290e-02,
       -9.67132673e-03, -1.67504624e-01, -1.58008978e-01, -2.39680618e-01,
        8.63035619e-02,  1.96732923e-01, -2.39867374e-01,  1.76191032e-02,
        1.94660947e-02, -3.50507259e-01,  9.82546881e-02, -6.53978214e-02,
       -6.43791929e-02,  4.53333199e-01, -6.74494356e-02,  2.05725431e-01,
        2.48260736e-01, -7.96512291e-02, -5.09492718e-02, -1.25820830e-01,
       -2.54160523e-01, -3.79837900e-01,  2.80270666e-01, -3.11355531e-01,
        1.00218251e-01, -2.05609590e-01,  2.66070187e-01,  8.94064456e-02,
       -1.07371770e-02,  2.40043029e-01, -3.06421995e-01,  1.17282093e-01,
        3.43994856e-01,  4.15822655e-01,  3.53698075e-01, -1.66001134e-02,
        1.70777529e-01,  2.12122381e-01,  3.01528424e-01,  2.12741643e-01,
       -5.18686846e-02, -3.47433031e-01, -6.92527741e-02,  3.57651487e-02,
       -3.31603646e-01, -3.69263813e-04, -1.68300420e-01,  1.93854436e-01,
       -6.24747396e-01,  1.61039904e-01,  8.47394615e-02,  2.06767067e-01,
        4.66150790e-02, -7.44918957e-02, -3.45102772e-02, -3.20701659e-01,
       -3.42431366e-01, -5.86029142e-02,  6.83633164e-02, -1.02490783e-01,
        6.36696041e-01,  1.32570788e-01,  1.58690363e-01,  3.81294265e-02,
       -5.66475019e-02,  6.83784112e-02, -4.77102280e-01, -1.03913136e-01,
        8.89730901e-02, -2.87425101e-01,  5.73363453e-02,  1.15170069e-01,
        1.89466134e-01,  6.39624596e-01, -8.51168483e-02, -3.60581815e-01,
       -1.81596681e-01, -2.13025436e-01, -4.08005752e-02,  4.65302579e-02,
        3.41815859e-01, -1.99242339e-01,  7.80186802e-02, -5.27780056e-01,
        2.82428525e-02,  1.70625314e-01,  3.02529037e-01, -4.11704779e-01,
        4.66627598e-01, -1.83744505e-01, -3.16921324e-02,  1.53818876e-01,
        4.90186781e-01,  2.14054421e-01, -1.60516083e-01,  7.45202303e-02,
        1.21610574e-01, -4.61614281e-02, -1.17486995e-02,  6.94388300e-02,
       -4.38876003e-02, -9.56380665e-02, -2.32885092e-01, -1.20004788e-01,
        1.78852260e-01,  1.93957791e-01, -3.25115919e-01,  4.77839857e-01,
        4.58942592e-01, -3.27724904e-01, -8.89120027e-02, -2.04065740e-02,
        2.04788655e-01, -2.69905508e-01,  5.66360801e-02,  4.83344868e-02,
       -9.87714082e-02,  2.36721411e-01, -3.72040048e-02,  2.03286022e-01,
        1.66709945e-02, -1.66082636e-01, -9.37711298e-02, -2.21098423e-01,
       -3.18903625e-02, -4.37021047e-01,  4.80386466e-02,  2.52574652e-01,
       -1.64837211e-01, -8.02500471e-02, -4.20770533e-02,  1.04366593e-01,
        7.25300610e-02, -2.12213725e-01,  1.78134337e-01,  2.10470125e-01,
        2.63405830e-01,  4.94371802e-02,  3.62759531e-01, -2.30380595e-01,
       -1.23702139e-01,  1.24911368e-01, -3.81581336e-01,  2.54870623e-01,
       -5.17856516e-03,  2.62863874e-01, -1.30387306e-01,  3.96716535e-01,
       -2.57542849e-01, -2.61414707e-01, -1.46659076e-01, -9.41694155e-02,
        3.98602307e-01, -3.37940693e-01, -7.92656362e-01, -2.23826364e-01,
       -3.22030425e-01,  3.87343913e-01, -2.41344765e-01, -1.09332621e-01,
       -5.45409203e-01, -3.60266924e-01,  3.70554656e-01,  2.65655071e-02,
       -2.53719985e-01,  4.41201538e-01, -3.97166491e-01,  8.13926682e-02,
       -1.01662669e-02,  9.75128412e-02,  3.28637183e-01,  1.94734722e-01,
       -9.46725011e-02, -1.92454487e-01,  3.29065114e-01,  2.31926084e-01,
        1.21656626e-01,  1.49020731e-01, -1.11507259e-01,  4.57766056e-01,
        2.81187836e-02, -2.48286948e-01, -1.87451795e-01,  2.67582357e-01,
        2.88918585e-01,  2.07469344e-01, -1.17748998e-01,  4.77143943e-01,
        7.09503964e-02,  4.33439016e-01, -2.51477063e-01,  1.71425074e-01,
        2.01444283e-01,  1.83082804e-01, -4.22960036e-02,  1.55468866e-01,
        2.57947482e-02, -2.85221517e-01, -4.18466568e-01,  4.66218889e-02,
       -2.63243794e-01,  3.96159858e-01,  3.41973603e-01,  2.39643931e-01,
        3.57474416e-01, -2.82690585e-01,  3.01905237e-02,  4.08621609e-01,
        8.58267173e-02,  3.27701747e-01,  2.60130912e-01,  3.79459083e-01]
        ],
        "job_ids": ["1"],
        }
    }


@app.get("/health_check")
def health_check():
    message = {"message": "Success", "status_code": 200}
    return Response(content=json.dumps(message), media_type="application/json")


@app.get("/count")
def get_count():
    count = collection.num_entities
    message = {"count": count}
    return Response(content=json.dumps(message), media_type="application/json")


@app.get("/index_processing")
def index_processing():

    message = utility.index_building_progress(MILVUS_COLLECTION)
    return Response(content=json.dumps(message), media_type="application/json")


@app.get("/load_index")
def load_index():
    collection.load()
    message = {"message": "Success", "status_code": 200}
    return Response(content=json.dumps(message), media_type="application/json")


@app.post("/search")
async def search_data(data: SearchDataInput):

    try:
        embeddings = np.array(data.embeddings).tolist()
        results = collection.search(
            data=embeddings,
            anns_field="embeddings",
            param=search_params,
            limit=5,
            expr=None,
        )
        distance_list = [i.distances for i in results]
        job_ids = [i.ids for i in results]
        result_json = {"distances": str(distance_list), "job_ids": str(job_ids)}
        message = result_json

    except Exception as e:
        logging.exception("Error occurred while searching data: {}".format(str(e)))
        raise HTTPException(status_code=500, detail=str(e))
    return Response(content=json.dumps(message), media_type="application/json")


@app.put("/insert")
def insert_data(data: InsertDataInput):
    embeddings = data.embeddings
    job_ids = data.job_ids

    temp_data = [job_ids, embeddings]
    insrt_flag = collection.insert(temp_data)
    message = {
        "insert_count": insrt_flag.insert_count,
        "timestamp": insrt_flag.timestamp,
        "success": insrt_flag.succ_count,
    }
    return Response(content=json.dumps(message), media_type="application/json")
