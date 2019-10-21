$(function () {
    $("[data-toggle='tooltip']").tooltip()
})

function setActiveLinks(){

    setActiveCategory();
    setActiveOrder();

}

function setActiveCategory(){
    // get menu items
    let menu = document.getElementsByClassName('btn-outline-secondary');
    let activeCategory = false;

    for ( let i = 0; i < menu.length; i++ ) {
        // if data-link is in url path
        if( menu[i].dataset.link == location.pathname ){
            menu[i].classList.add('active');
            activeCategory = true;
        }
        else{
            // if data-idname is in search path (?id=THIS) (member search)
            let params = new URLSearchParams(location.search);
            if( params.has('id') && menu[i].dataset.idname == params.get('id') ){
                menu[i].classList.add('active');
                activeCategory = true;
            }
        }
        // hide orders by time on "last comment" page
        if( location.pathname == '/commented/' ){
            document.getElementById('order-group').style.display = 'none';
        }
    }

    if ( ! activeCategory )
        menu[0].classList.add('active');
}

function setActiveOrder(){

    let params = new URLSearchParams(location.search);

    // get elements
    let orders = [
        document.getElementById('order-oldest'),
        document.getElementById('order-newest')
    ];

    // no order is currently set
    let activeOrder = false;

    for (i of orders ){
        // create link with right parameters
        createLinkOrder(i, i.dataset.url);

        // if data-url is in search path (?order=THIS)
        if ( params.has('order') && i.dataset.url == params.get('order') ){
            i.classList.add('active');
            activeOrder = true;
        }
    }

    // default order is none is set
    if ( ! activeOrder )
        orders[1].classList.add('active');

}

function createLinkOrder(e, param){
    var params = new URLSearchParams(location.search);
    
    if ( ! params.has('order') )
        params.append('order', param);
    else
        params.set('order', param);
    e.href = '?' + params;
}


setActiveLinks();


// detecting sticky position in order to display tasks count in menu

let observer = new IntersectionObserver(function(entries) {
	// no intersection with screen
	if(entries[0].intersectionRatio === 0){
		document.getElementById('fixed-infos').style.opacity = 1;
    }
	// fully intersects with screen
	else if(entries[0].intersectionRatio === 1)
    document.getElementById('fixed-infos').style.opacity = 0;
}, { threshold: [0,1] });

observer.observe(document.querySelector("#hackish-way-of-detecting-sticky-in-js"));