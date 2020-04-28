pandoc --template eisvogel --listings \
   --toc --number-sections \
   -V title:"COT 6405 Programming Project" \
   -V author:"Christian Garbin" \
   -V margin-top:"2cm" \
   -V titlepage:true \
   -V titlepage-color:99CCFF \
   -V toc-own-page:true \
   -V header-left:"COT 6405 Spring 2020" \
   -V header-right:"Longest Common Subsequence" \
   -V code-block-font-size:"\scriptsize" \
   lcs-experiments.ipynb -o lcs-experiments.pdf
