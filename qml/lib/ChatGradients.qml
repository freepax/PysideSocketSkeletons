import QtQuick 1.0

Item {
    id: gfour

    //property alias off: goff
    property alias off: grad
    property alias onn: gonn
    property alias rad: grad

    Gradient {
        id: goff
        GradientStop { id: offfirst; position: 0.0; color: "lightsteelblue" }
        GradientStop { id: offsecond; position: 0.5; color: "lightsteelblue" }
        GradientStop { id: offthird; position: 0.5; color: "black" }
        GradientStop { id: offfourth; position: 1.0; color: "black" }
    }

    Gradient {
        id: gonn
        GradientStop { id: onfirst; position: 0.0; color: "steelblue" }
        GradientStop { id: onsecond; position: 0.5; color: "steelblue" }
        GradientStop { id: onthird; position: 0.5; color: "black" }
        GradientStop { id: onfourth; position: 1.0; color: "black" }
    }

    Gradient {
        id: grad
        GradientStop { position: 0.0; color: "#8C8F8C" }
        GradientStop { position: 0.17; color: "#6A6D6A" }
        GradientStop { position: 0.98;color: "black" }
        GradientStop { position: 1.0; color: "black" }
    }
}
