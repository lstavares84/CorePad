"""RF64 PCM writer reference. Device audio/DMA/storage integration remains separate."""
import struct

class RF64Writer:
    def __init__(self, stream, channels=2, rate=48000):
        if channels not in (2,4) or rate!=48000:raise ValueError("Perfil PCM não suportado")
        self.stream=stream;self.align=channels*2;self.size=0;self.closed=False
        stream.write(b"RF64"+struct.pack("<I",0xffffffff)+b"WAVE")
        stream.write(b"ds64"+struct.pack("<IQQQI",28,0,0,0,0))
        stream.write(b"fmt "+struct.pack("<IHHIIHH",16,1,channels,rate,rate*self.align,self.align,16))
        stream.write(b"data"+struct.pack("<I",0xffffffff))
    def write(self, pcm):
        if self.closed:raise ValueError("Arquivo já encerrado")
        if len(pcm)%self.align:raise ValueError("Bloco deve conter frames completos")
        written=self.stream.write(pcm)
        if written!=len(pcm):raise OSError("Escrita parcial de áudio")
        self.size+=written
    def close(self):
        if self.closed:return
        end=self.stream.tell();self.stream.seek(20)
        self.stream.write(struct.pack("<QQQ",end-8,self.size,self.size//self.align))
        self.stream.seek(end);self.stream.flush();self.closed=True
