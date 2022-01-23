(function (window, document, undefined) {

	document.addEventListener('DOMContentLoaded', initialize);

	function initialize() {
		var container = document.getElementById('av-orbit');
		container.style.overflow = 'hidden';
		container.innerHTML = getHTML();
	}

	function getHTML() {
		var size   = 'medium';
		const HEIGHTS = { small: 120, medium: 160, large: 100 };
		const WIDTHS  = { small: 300, medium: 400, large: 500 };
		const TEXTFIELD_HEIGHT = 107;
		
		var p = avOrbitProperties;   // from global variable
		if (p.size && ['small', 'medium', 'large'].includes(p.size)) {
			size = p.size;
		}
		var height = HEIGHTS[size] + TEXTFIELD_HEIGHT;
		var width  = WIDTHS[size];
		var lang  = (p.lang && ['de'].includes(p.lang)) ? p.lang : 'en';

		var url = 'https://astroviewer.net/iss/widgets/orbit-widget.php?size=' + size + '&lang=' + lang;
//		var url = 'http://localhost:8058/SatPasses2/widgets/orbit-widget.php?size=' + size + '&lang=' + lang;

		var x = '';
		x += '<iframe id="orbit-iframe" src="' + url + '" sandbox="allow-scripts allow-same-origin allow-popups" scrolling="no" style="overflow:hidden; border: 1px solid #ccc;"></iframe>';
		return x;
	}

}) (window, document);