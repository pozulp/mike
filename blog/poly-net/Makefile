equation_dpi=60
figure_dpi=100
table_dpi=$(figure_dpi)

all: poly_eqn.png net_fig.png loss_eqn.png code_table.png conv_crit_eqn.png solution_plot.png loss_plot.png model_inputs_table.png version_table.png

poly_eqn.png: poly_eqn.tex
	pdflatex poly_eqn.tex
	pdftoppm poly_eqn.pdf poly_eqn -png -f 1 -singlefile -rx $(equation_dpi) -ry $(equation_dpi)
	magick poly_eqn.png -trim poly_eqn.png

net_fig.png: net_fig.tex
	pdflatex net_fig.tex
	pdftoppm net_fig.pdf net_fig -png -f 1 -singlefile -rx $(figure_dpi) -ry $(figure_dpi)
	magick net_fig.png -trim net_fig.png

loss_eqn.png: loss_eqn.tex
	pdflatex loss_eqn.tex
	pdftoppm loss_eqn.pdf loss_eqn -png -f 1 -singlefile -rx $(equation_dpi) -ry $(equation_dpi)
	magick loss_eqn.png -trim loss_eqn.png

code_table.png: code_table.tex
	pdflatex code_table.tex
	pdftoppm code_table.pdf code_table -png -f 1 -singlefile -rx $(table_dpi) -ry $(table_dpi)
	magick code_table.png -trim code_table.png

conv_crit_eqn.png: conv_crit_eqn.tex
	pdflatex conv_crit_eqn.tex
	pdftoppm conv_crit_eqn.pdf conv_crit_eqn -png -f 1 -singlefile -rx $(equation_dpi) -ry $(equation_dpi)
	magick conv_crit_eqn.png -trim conv_crit_eqn.png

solution_plot.png: poly.py plot.py
loss_plot.png: poly.py plot.py
	./poly.py -3 3
	./plot.py -3 3 --interval 2000
	magick solution_plot.png -trim -resize 400x300 solution_plot.png
	magick loss_plot.png -trim -resize 400x300 loss_plot.png

model_inputs_table.png: model_inputs_table.tex
	pdflatex model_inputs_table.tex
	pdftoppm model_inputs_table.pdf model_inputs_table -png -f 1 -singlefile -rx $(table_dpi) -ry $(table_dpi)
	magick model_inputs_table.png -trim model_inputs_table.png

version_table.png: version_table.tex
	pdflatex version_table.tex
	pdftoppm version_table.pdf version_table -png -f 1 -singlefile -rx $(table_dpi) -ry $(table_dpi)
	magick version_table.png -trim version_table.png

clean:
	rm -f poly_eqn.aux poly_eqn.log poly_eqn.pdf
	rm -f net_fig.aux net_fig.log net_fig.pdf
	rm -f loss_eqn.aux loss_eqn.log loss_eqn.pdf
	rm -f code_table.aux code_table.log code_table.pdf
	rm -f conv_crit_eqn.aux conv_crit_eqn.log conv_crit_eqn.pdf
	rm -f poly.args.dat  poly.loss_history.dat  poly.model.dat  poly.pred_history.dat
	rm -f model_inputs_table.aux model_inputs_table.log model_inputs_table.pdf
	rm -f version_table.aux version_table.log version_table.pdf

