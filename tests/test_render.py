import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('render',ROOT/'skills/food-product-cards/scripts/render.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RenderTests(unittest.TestCase):
 def setUp(self): self.d=json.loads((ROOT/'examples/demo.json').read_text());self.base=ROOT/'examples'
 def test_offline(self):
  out=m.render(self.d,self.base);self.assertEqual(out.count('<article'),2);self.assertIn('data:image/svg+xml;base64,',out);self.assertNotIn('<div',out)
 def test_escaping(self):
  self.d['products'][0]['name']='<script>alert(1)</script>';self.assertIn('&lt;script&gt;',m.render(self.d,self.base))
 def test_missing_strategy(self):
  self.d['products'][0]['sections'][2]['body']='';self.assertRaises(ValueError,m.render,self.d,self.base)
 def test_missing_image(self):
  self.d['products'][0]['photo']='absent.png';self.assertRaises(FileNotFoundError,m.render,self.d,self.base)
 def test_labels(self):
  self.d['products'][0]['labels'][0]['y']=101;self.assertRaises(ValueError,m.render,self.d,self.base)
 def test_duplicate(self):
  self.d['products'].append(copy.deepcopy(self.d['products'][0]));self.assertRaises(ValueError,m.render,self.d,self.base)
 def test_menu_order(self):
  p=copy.deepcopy(self.d['products'][0]);p['id']='second';p['name']='SECOND';self.d['products'].append(p)
  self.d['menu'][0]['items'][0]['new']=False;self.d['menu'][0]['items'].append({'product_id':'second','price':'22','new':True})
  out=m.render(self.d,self.base);self.assertLess(out.index('id="second"'),out.index('id="demo"'))
 def test_unknown_product(self):
  self.d['menu'][0]['items'][0]['product_id']='absent';self.assertRaises(ValueError,m.render,self.d,self.base)
if __name__=='__main__': unittest.main()
