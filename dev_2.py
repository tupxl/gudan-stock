# UTILITY
def gen_counter():
    ''' Fungsi membuat generator unique key
    Generator unique key atau counter
    '''
    counter = 0
    while(True):
        yield counter
        counter += 1

def get_ID():
    ''' Fungsi untuk mendapatkan unique key
    Fungsi initialize harus dijalankan dulu
    '''
    global primary_keys, gen_pk
    
    pk = next(gen_pk)
    primary_keys.add(pk)
    
    return pk

def get_num_item():
    ''' Mendapatkan jumlah item (datum)
    menghitung panjang dictionary yang menyimpan
    data stock.
    '''
    global primary_keys
    
    return len(primary_keys)



def initialize(predata=False):
    ''' Fungsi inisialisasi
    Fungsi ini digunakan untuk menciptakan variabel
    dan generator.
    Input   :(bool) predata -> Inisiasi dengan data awal
    Output  :(None)

    Generate:
        - gen_pk = generator unique key
        - primary_keys = menyimpan unique key
        - stock = dictionary penyimpanan data
        - columns = data yang bisa diisi (field)
        - template_stock = template data
    '''
    global gen_pk, primary_keys, stock, columns, template_stock
    
    gen_pk = gen_counter()
    primary_keys = set()
    stock = dict()
    columns = { # Mendefinisikan field, tipe, dan limit.
        'Nama':{'type':str, 'limit':25},
        'Jumlah':{'type':int, 'limit':99},
        'Harga':{'type':int, 'limit':99},
        'Satuan':{'type':str, 'limit':25},
        'Kategori':{'type':str, 'limit':25},
    }

    template_stock = dict.fromkeys(columns.keys())

    if predata: # Membuat data awal
        ID = get_ID()
        stock[ID] = {
            'Nama':'Aqua',
            'Jumlah':30,
            'Harga':1500,
            'Satuan':'Satuan',
            'Kategori':'Minuman',
        }

        ID = get_ID()
        stock[ID] = {
            'Nama':'Gas Hijau',
            'Jumlah':30,
            'Harga':2000,
            'Satuan':'Satuan',
            'Kategori':'Bahan Bakar',
        }
    
    return 0

def confirmation(perubahan, nama, no_id=False):
    ''' Fungsi untuk konfirmasi perubahan data
    menggunakan fungsi view_datum dan y_or_n,
    untuk melihat perubahan dan menerima jawaban.

    Input   :-(dict) perubahan = data yang ingin diubah
             -(str) nama = kata perubahan yang ingin
                            ditampilkan
             -(bool) no_id = untuk fungsi view_datum
    '''
    print('\nKonfirmasi ' + nama)
    view_datum(perubahan, no_id)
    choice = y_or_n()
    if choice:
        return True
    
    return False

def check_input(col, unique=False):
    ''' Fungsi untuk memeriksa input pada field
    Input   :-(str) col = nama field
             -(bool) unique = apakah jika field nama harus unique atau tidak
    Output  :Value yang telah tervalidasi
    '''
    status = True
    acc_type = columns[col]['type']
    limit_char = columns[col]['limit']
    while(status):
        try:
            user_input = input(f'Masukkan {col:<{15}}:')
            if limit_char<len(user_input)<0: # Pembatasan karakter
                raise Exception
            value = acc_type(user_input)
            if unique and col=='Nama': # Nama harus unique
                for info in stock.values():
                    if info['Nama'] == value:
                        raise NameError
        except ValueError: # Cek tipe
            print(f'\n[ERROR] Tipe untuk {col} adalah {str(acc_type)}, mohon cek kembali!')
        except NameError: # Jika nama sudah ada
            print(f'\n[ERROR] Produk dengan nama {value} sudah ada')
        except Exception: # Melebihi batas karakter
            print(f'\n[ERROR] Input melebihi batas maksimal karakter, hanya menerima {limit_char} karakter')
        else:
            status = False
    return value

def y_or_n(custom=''):
    ''' Fungsi untuk menerima jawaban Y atau N
    Melakukan check input apakah sesuai Y atau N
    Input   :(str) custom = akan menampilkan custom teks jika diisi
    Output  :(bool) user_input = True untuk Y dan False untuk N
    '''
    status = True
    if len(custom)==0:
        question = 'Apakah kamu yakin melakukan perubahan ini? [Y/N]\t:'
    else:
        question = custom
    while(status):
        user_input = input(question)
        if 'y'==user_input.lower():
            user_input=True
            status = False
        elif 'n'==user_input.lower():
            user_input=False
            status = False
        else:
            print(f'[ERROR] Hanya menerima Y/N')
    return user_input

def pilihan(list_pilihan,block):
    ''' Fungsi untuk menerima jawaban nomor
    Melakukan check input apakah sesuai dengan nomor
    Input   :(list->int) list_pilihan = List pilihan, paling akhir adalah exit
    Output  :(int) pilihan = Bilangan integer
    '''
    status = True
    print(block)
    while(status):
        try:
            pilihan = int(input('\nMasukkan pilihan yang ingin dijalankan\t:'))
            if pilihan in list_pilihan:
                status = False
            else:
                print('\n[ERROR] Harap masukkan pilihan yang sesuai')
        except ValueError:
            print('\n[ERROR] Harap masukkan pilihan yang sesuai')
    
    return pilihan


def get_stock(ID):
    ''' Fungsi untuk mengambil stock dari ID
    Input   :(int) ID = ID dari produk (unique keys)
    Output  :-(bool) status = True or False, ada atau tidak
             -(dict) stock = jika status True akan mengembalikan dict
             -(str) pesan = jika status False akan mengembalikan pesan
    '''
    pesan = ''
    try:
        return True, stock[ID]
    except KeyError:
        pesan += f'[ERROR] Tidak ada ID {ID}'
        return False, pesan

# MELIHAT DATA
def view_header(no_id=False):
    ''' Mencetak header dari kolom
    Input   :(bool) no_id = Apakah menampilkan ID atau tidak
    '''
    n_column = len(columns)
    if no_id:
        num_decor = (n_column) + ((n_column)*15)-1
        print('+'+'-'*num_decor+'+')
        text = "|"
    else:
        num_decor = (n_column+1) + ((n_column+1)*15)-1
        print('+'+'-'*num_decor+'+')
        text = f"|{'ID':^{15}}|"
    for info in columns.keys():
        text += f'{info:^{15}}|'
    print(text)
    print('+'+'-'*num_decor+'+')

def view_all():
    ''' Mencetak semua data yang ada
    '''
    if get_num_item():
        view_header()
        for key, value in stock.items():
            text = f"|{key:^{15}}|"
            for info in value.values():
                text += f'{info:^{15}}|'
            print(text)
    else:
        print('\n[ERROR] Tidak ada data')

def view_selected(pk=[], no_id=False):
    ''' Mencetak semua data dipilih
    Input   :(bool) no_id = Apakah menampilkan ID atau tidak
    '''
    pk.sort()
    if get_num_item():
        view_header(no_id)
        for key in pk:
            text = f"|{key:^{15}}|"
            status, dump = get_stock(key)
            if status:
                for info in dump.values():
                    text += f'{info:^{15}}|'
                print(text)
            else:
                print(dump)
    else:
        print('\n[ERROR] Tidak ada data')

def view_datum(datum,no_id=True):
    ''' Mencetak dictionary 
    Input   :-(dict) datum = dictionary mengikuti template stock
             -(bool) no_id = Apakah menampilkan ID atau tidak
    '''
    view_header(no_id)
    text = '|'
    for info in datum.values():
        text += f'{info:^{15}}|'
    print(text)

def view_selected_wrapper():
    ''' Wrapper atau interface untuk view_selected
    '''
    status = False
    while(not status): 
        pesan = ''
        try:
            ID = list(map(int,input('\nMasukkan ID yang ingin dilihat\t:').split(',')))
            for i in ID:
                status, dump = get_stock(i)
                if not status:
                    pesan += dump+'\n'
            
        except ValueError:
            print('\n[ERROR] Hanya menerima ID berupa bilangan integer positif')
        else:
            if len(pesan)!=0:
                print(pesan)
    view_selected(ID)



# MENAMBAHKAN STOCK
def create_stock():
    ''' Funsgi untuk menambahkan stock baru
    Mengatasi duplikasi yang ada pada nama
    '''
    global gen_pk, stock
    
    new_stock = template_stock.copy()
    for key in new_stock.keys():
        new_stock[key] = check_input(key,unique=True)
  
    else:
        if confirmation(new_stock, 'Tambah Product', no_id=True):
            ID = get_ID()
            stock[ID] = new_stock
            print(f'\n[SUCCESS] Produk dengan ID {ID} berhasil dibuat')

# UPDATE
def update_stock(ID):
    ''' Fungsi untuk memperbarui stock
    Memperbarui berdasarkan ID
    Input   :(int) ID = ID dari stock yang ingin dihapus
    '''
    global stock
    status, dump = get_stock(ID)
    if status:
        view_selected([ID])
        if y_or_n(custom='Apakah anda ingin melanjutkan?[Y/N]\t:'):
            keys = keys_input()
            new_stock = dump.copy()
            new_stock = {'ID':ID, **new_stock}
            for key in keys:
                new_stock[key] = check_input(key,unique=True)

            if confirmation(new_stock, 'Update Product', False):
                for key in keys:
                    stock[ID][key] = new_stock[key]
                print(f'[SUCCESS] Produk dengan ID {ID} berhasil diperbarui')
    else:
        print(dump)  

def keys_input():
    ''' Fungsi untuk menerima input keys (field)
    Keys (field) yang dimasukkan harus sesuai dengan yang ada
    '''
    status = True
    while(status):
        keys = input('\nMasukkan kolom yang ingin diubah (Pisahkan dengan koma):').split(',')
        keys = [key.strip().capitalize() for key in keys if key != '' ]
        existing = [col for col in columns.keys()]
        for key in keys:
            if key not in existing:
                print(f'[ERROR] {key} tidak ada di kolom')
                break
        else:
            status = False
            
    return keys

def update_wrapper():
    ''' Fungsi untuk interface update_stock
    '''
    status = False
    while(not status): 
        try:
            ID = int(input('\nMasukkan ID yang ingin diubah\t:'))
            status, dump = get_stock(ID)
        except ValueError:
            print('\n[ERROR] Hanya menerima ID berupa bilangan integer positif')
        else:
            if type(dump)==str:
                print(dump)
    update_stock(ID) 

# DELETE 
def delete_stock(ID):
    ''' Fungsi untuk menghapus stock
    Menghapus stock berdasarkan ID
    
    Input   :(int) ID = ID/unique key stock
    '''
    global stock
    view_selected([ID])
    choice = y_or_n()
    if choice:
        del stock[ID]
        print(f'[SUCCESS] Stock dengan ID {ID} berhasil dihapus')
      

def delete_wrapper():
    ''' Interface untuk delete_stock
    '''
    status = False
    while(not status): 
        try:
            ID = int(input('\nMasukkan ID yang ingin dihapus\t:'))
            status, dump = get_stock(ID)
        except ValueError:
            print('\n[ERROR] Hanya menerima ID berupa bilangan integer positif')
        else:
            if type(dump)==str:
                print(dump)
    delete_stock(ID)


# MENU
def main_menu():
    ''' Fungsi untuk menampilkan Main Menu'''
    block = ''' 
    Selamat Datang di Gudang
    
    List Menu:
    1. Menampilkan Daftar Stock
    2. Menambahkan Stock
    3. Menghapus Stock
    4. Update Stock
    5. Exit Program
    '''

    return pilihan([1,2,3,4,5], block)

def menu_view():
    '''Fungsi untuk menampilkan menu daftar'''
    menu=f'''
    {" Melihat Stock ":+^{50}}
    1. Lihat semua
    2. Lihat tertentu
    3. Kembali ke menu utama
    '''
    pil = pilihan([1,2,3],menu)
    while(pil!=3):
        if len(stock)==0:
            print('\n[ERROR] Tidak ada data')
        else:
            if pil==1:
                view_all()
            else:
                view_selected_wrapper()
        pil = pilihan([1,2,3],menu)

def menu_create():
    '''Fungsi untuk menampilkan menu tambah'''
    menu=f'''
    {" Menambahkan Stock ":+^{50}}
    1. Menambahkan stock baru
    2. Kembali ke menu utama
    '''
    pil = pilihan([1,2],menu)
    while(pil!=2):
        if pil==1:
            create_stock()
        pil = pilihan([1,2],menu)

def menu_delete():
    '''Fungsi untuk menampilkan menu hapus'''
    menu=f'''
    {" Menghapus Stock ":+^{50}}
    1. Menghapus stock
    2. Kembali ke menu utama
    '''
    pil = pilihan([1,2],menu)
    while(pil!=2):
        if len(stock)==0:
            print('\n[ERROR] Tidak ada data')
        else:
            if pil==1:
                delete_wrapper()
        pil = pilihan([1,2],menu)


def menu_update():
    '''Fungsi untuk menampilkan menu perbarui'''
    menu=f'''
    {" Memperbarui Stock ":+^{50}}
    1. Pebarui stock
    2. Kembali ke menu utama
    '''
    pil = pilihan([1,2],menu)
    while(pil!=2):
        if len(stock)==0:
            print('\n[ERROR] Tidak ada data')
        else:
            if pil==1:
                update_wrapper()
        pil = pilihan([1,2],menu)

def main():
    '''Fungsi yang akan dijalankan'''

    initialize(predata=True) # Inisiasi
    pilihan = main_menu() # Menampilkan main menu dan menerima pilihan
    while pilihan != 5:
        if pilihan == 1: 
            menu_view()
        elif pilihan == 2:
            menu_create()
        elif pilihan == 3:
            menu_delete()
        else:
            menu_update()

        pilihan = main_menu()

if __name__ =='__main__':
    main()