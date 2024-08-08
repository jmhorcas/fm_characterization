// import { get_property } from './fm_fact_label.js';

/**
 * Set-up the save PNG button.
 */
d3.select('#savePNG').on('click', () => handleSave(rasterize, ".png", "image/png"));

/**
 * Set-up the save SVG button.
 */
d3.select('#saveSVG').on('click', () => handleSave(serializeToSVG, ".svg", "image/svg+xml"));

/**
 * Set-up the save PDF button.
 */
d3.select('#savePDF').on('click', async () => {
    const chart = d3.select(".chart");
    const svgElement = chart.node();
    const originalHeight = adjustSVGSize(svgElement);

    try {
        const bbox = svgElement.getBBox();
        const blob = await rasterize(svgElement);
        const imgData = await readBlobAsDataURL(blob);

        const data = typeof fmData !== 'undefined' ? fmData : fmDataSetData;
        const name = get_property(data, 'Name').value;

        const pdf = new jspdf.jsPDF({
            orientation: (bbox.width > bbox.height) ? 'landscape' : 'portrait',
            unit: 'pt',
            format: [bbox.width, bbox.height]
        });

        pdf.addImage(imgData, 'PNG', 0, 0, bbox.width, bbox.height);
        pdf.save(name + ".pdf");
    } catch (error) {
        console.error("An error occurred while saving the PDF:", error);
    } finally {
        restoreSVGSize(svgElement, originalHeight);
        newData = filterData(ALL_DATA);
        redrawLabel(newData);
    }
});

/**
 * Set-up the save TXT button.
 */
d3.select('#saveTXT').on('click', function () {
    const data = typeof fmData !== 'undefined' ? fmData : fmDataSetData;
    var blob = new Blob([fmCharacterizationStr], { type: "text/plain" });
    saveAs(blob, get_property(data, 'Name').value + ".txt");
});

/**
 * Set-up the save JSON button.
 */
d3.select('#saveJSON').on('click', function () {
    const data = typeof fmData !== 'undefined' ? fmData : fmDataSetData;
    var blob = new Blob([fmCharacterizationJSONStr], { type: "application/json" });
    saveAs(blob, get_property(data, 'Name').value + ".json");
});

/**
 * Generic code to download a file available on the server.
 * (Not used actually.)
 */
function downloadUsingAnchorElement() {
    const anchor = document.createElement("a");
    anchor.href = IMG_URL;
    anchor.download = FILE_NAME;
    
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
}

/**
 * Third-party code:
 * - For saving SVG and PNG: https://observablehq.com/@mbostock/saving-svg
 * - FileSaver (for saving files on the client-side): https://github.com/eligrey/FileSaver.js/
 */

const xmlns = "http://www.w3.org/2000/xmlns/";
const xlinkns = "http://www.w3.org/1999/xlink";
const svgns = "http://www.w3.org/2000/svg";

function serializeToSVG(svg) {
    svg = svg.cloneNode(true);
    const fragment = window.location.href + "#";
    const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT);
    while (walker.nextNode()) {
        for (const attr of walker.currentNode.attributes) {
            if (attr.value.includes(fragment)) {
                attr.value = attr.value.replace(fragment, "#");
            }
        }
    }
    svg.setAttributeNS(xmlns, "xmlns", svgns);
    svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
    const serializer = new XMLSerializer();
    const string = serializer.serializeToString(svg);
    return new Blob([string], { type: "image/svg+xml" });
}

function rasterize(svg) {
    let resolve, reject;
    const promise = new Promise((y, n) => (resolve = y, reject = n));
    const image = new Image();
    image.onerror = (e) => {
        console.error("Image onerror event:", e);
        reject(e);
    };
    image.onload = () => {
        const rect = svg.getBoundingClientRect();
        const context = context2d(rect.width, rect.height);
        context.drawImage(image, 0, 0, rect.width, rect.height);
        context.canvas.toBlob((blob) => {
            resolve(blob);
        }, 'image/png');
    };
    const serializedSVG = serializeToSVG(svg);
    image.src = URL.createObjectURL(serializedSVG);
    return promise;
}

function context2d(width, height, dpi) {
    if (dpi == null) dpi = devicePixelRatio;
    const canvas = document.createElement("canvas");
    canvas.width = width * dpi;
    canvas.height = height * dpi;
    canvas.style.width = width + "px";
    const context = canvas.getContext("2d");
    context.scale(dpi, dpi);
    return context;
}

const adjustSVGSize = (svgElement) => {
    const originalHeight = svgElement.getAttribute("height");

    d3.select(".chart").selectAll("#collapseIcon").attr("visibility", "hidden");

    const bbox = svgElement.getBBox();
    svgElement.setAttribute("height", bbox.height);

    return originalHeight;
};

const restoreSVGSize = (svgElement, originalHeight) => {
    svgElement.setAttribute("height", originalHeight);
};

const readBlobAsDataURL = (blob) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(new Error("Error reading the blob"));
        reader.readAsDataURL(blob);
    });
};

const handleSave = async (serializeFunction, extension) => {
    const chart = d3.select(".chart");
    const svgElement = chart.node();
    const originalHeight = adjustSVGSize(svgElement);

    try {
        const blob = await serializeFunction(svgElement);

        const data = typeof fmData !== 'undefined' ? fmData : fmDataSetData;
        const name = get_property(data, 'Name').value;

        if (typeof extension !== 'string') {
            throw new TypeError('Extension must be a string');
        }

        saveAs(blob, name + extension);
    } catch (error) {
        console.error(`An error occurred while saving the ${extension.toUpperCase()}:`, error);
    } finally {
        restoreSVGSize(svgElement, originalHeight);
        newData = filterData(ALL_DATA);
        redrawLabel(newData);
    }
};
