import io
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"software"))
from device import Simulator, default_config, validate
from rf64 import RF64Writer
from wire_protocol import encode, decode, json_payload, simulator_exchange, GET_CONFIG, SET_CONFIG, CONFIG, ACK

class ConfigurationTests(unittest.TestCase):
    def test_portuguese_capacity(self):
        c=default_config();c['macros'][0][0]='ç'*256
        self.assertEqual(len(validate(c)['macros'][0][0]),256)
        c['macros'][0][0]+='a'
        with self.assertRaises(ValueError):validate(c)
    def test_transaction_and_secret_boundary(self):
        device=Simulator();c=default_config();c['rgb']['brightness']=-1
        with self.assertRaises(ValueError):device.request({'command':'set_config','config':c})
        self.assertEqual(device.config,default_config())
        for command in ('unlock','export_secrets','authenticate'):
            with self.assertRaises(ValueError):device.request({'command':command})
        c=default_config();c['macros'].append(['']*9)
        with self.assertRaises(ValueError):validate(c)
    def test_rgb_and_copy(self):
        device=Simulator();c=default_config();c['rgb']['color']='#2255ff'
        device.request({'command':'set_config','config':c});c['rgb']['color']='#000000'
        self.assertEqual(device.config['rgb']['color'],'#2255ff')
    def test_rf64_sizes(self):
        stream=io.BytesIO();writer=RF64Writer(stream,channels=4);writer.write(bytes(800));writer.close()
        blob=stream.getvalue();self.assertEqual(blob[:4],b'RF64')
        self.assertEqual(struct.unpack_from('<QQQ',blob,20),(len(blob)-8,800,100))
        with self.assertRaises(ValueError):writer.write(bytes(8))
    def test_incomplete_frame(self):
        writer=RF64Writer(io.BytesIO())
        with self.assertRaises(ValueError):writer.write(b'123')
    def test_public_frame_and_transaction(self):
        sim=Simulator(); config=default_config();config['rgb']['color']='#ff6a00'
        reply=simulator_exchange(sim,encode(SET_CONFIG,42,json_payload(config)))
        self.assertEqual(decode(reply),(ACK,42,b''))
        result=decode(simulator_exchange(sim,encode(GET_CONFIG,43)))
        self.assertEqual((result[0],result[1]),(CONFIG,43))
        self.assertIn(b'#ff6a00',result[2])
        bad=bytearray(encode(GET_CONFIG,44));bad[-1]^=1
        with self.assertRaisesRegex(ValueError,'CRC'):simulator_exchange(sim,bytes(bad))
        self.assertEqual(sim.config,config)
        with self.assertRaisesRegex(ValueError,'comprimento'):decode(encode(GET_CONFIG,44)+b'x')

if __name__=='__main__':unittest.main()
