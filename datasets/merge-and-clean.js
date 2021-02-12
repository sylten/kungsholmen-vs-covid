const fs = require('fs')
const json2csv = require('json-2-csv').json2csv;

const hemnetDataDir = './hemnet-data';
const outputFile = './apartment-prices.csv';

function getFloor(adress) {
    for (let pattern of [/,(.*) tr/, /, (.*)tr/, /,(.*)tr/, /, våning (.*)/, /, vån (.*)/,/ vån (.*)./]) {
        let tr = adress.match(pattern);
        if (tr?.[1]) {
            return tr[1].trim()
        }
    }
    return '0';
}

const allApartments = {};

for (let i = 1; i <= 25; i++) {
    data = require(`${hemnetDataDir}/data${i}.json`);
    for (let p of data.properties) {
        p.price_per_area = p.price_per_area?.replace(/\D/g,'') || '';
        p.asked_price = p.asked_price?.replace(/\D/g,'') || '';
        p.price = p.formatted_price?.replace(/\D/g,'') || '';
        p.price_change = !p.formatted_price_change_percentage ? 0 : parseInt(p.formatted_price_change_percentage.replace(/[\+\%\s]/g,''));
        p.living_space = (p.living_space?.substr(0, p.living_space.indexOf(' ')).replace(',', '.') || '').trim();
        p.supplemental_area = p.supplemental_area?.substr(0, p.supplemental_area.indexOf(' ')).replace(',', '.') || 0;
        p.rooms = p.rooms?.substr(0, p.rooms.indexOf(' ')).replace(',', '.') || '';
        p.fee = p.fee?.replace(/\D/g,'') || '';
        p.floor = getFloor(p.address).match(/\d+/)?.shift() || '0'
        p.location_part = p.location_name?.split(',')[0] || ''
        p.street_id = p.address?.substr(0, p.address.match(/[^\D+$]/)?.index || p.address.length).replace(/[^A-z]/g, '').toLowerCase() || '';
        p.sale_date = p.sale_date?.substr(5) || '';
        p.latitude = p.coordinate[0];
        p.longitude = p.coordinate[1];

        if (p.floor.match(/[^\d]/g)) {
            console.log(`floor '${p.floor}' contains non-numeric characters`)
        }
        else if (parseInt(p.floor) > 15) {
            console.log(`floor ${p.floor} seems too high for Kungsholmen (${p.id})`)
        }

        if (p.rooms.indexOf('.') > -1) {
            p.rooms = p.rooms.substr(0, p.rooms.indexOf('.'));
        }

        allApartments[p.id] = p;
    }
}

const apartments = Object.keys(allApartments).map(key => allApartments[key]);

console.log(`found ${apartments.length} unique prices`)

json2csv(apartments, (err, csv) => {
    if (err) {
        throw err;
    }

    fs.writeFileSync(outputFile, csv);
});
