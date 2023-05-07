SRATE = 44100
MAX_CHUNK = 512
DECAY = 0.98

NOTAS = dict(C=523.241, D=587.33, E=659.255, F=698.56, G=783.991,
             A=880, B=987.767)

# Parámetros configurables
MODELS = ("sintetizador tunned", "sintetizador basic", "sampler")
CHUNK_SIZE = (64, 256, 512)