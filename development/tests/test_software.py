import io
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"software"))
from device import Simulator, default_config, validate
from rf64 import RF64Writer

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

if __name__=='__main__':unittest.main()
