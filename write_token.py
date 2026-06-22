import pathlib
p = pathlib.Path(r'C:\Users\abhay\.kaggle\access_token')
p.write_text('KGAT_ec4e1a08f5581770692d516e0766c9c1')
print('Written to:', p)
print('Content:', p.read_text())
