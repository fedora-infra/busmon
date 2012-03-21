<%inherit file="local:templates.master"/>
	<div class="content">
	${barchart.display() | n}
	</div>
	<div class="clear spacer"></div>
	<div class="content">
	${timeseries.display() | n}
	</div>
