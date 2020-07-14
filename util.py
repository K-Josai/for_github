
def show_progress(i, max_iter, prog_size=50):
    i+=1
    progressd_size = int(i/max_iter*prog_size)
    empty_size = int(prog_size - progressd_size)
    pro_bar = ('=' * progressd_size) + (' ' * empty_size)
    print('\r[{0}] {1}/{2}'.format(pro_bar, i, max_iter), end='')
    if i>=max_iter: print()
