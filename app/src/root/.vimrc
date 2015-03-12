:set expandtab
:set tabstop=4
:set paste
:set ruler
:set number
highlight OverLength ctermbg=darkred ctermfg=white guibg=#FFD9D9
match OverLength /\%>100v.\+/
