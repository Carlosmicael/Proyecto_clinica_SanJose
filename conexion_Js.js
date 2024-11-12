const mysql = require('mysql2');



const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root', 
    password: '', 
    database: 'universidad'
});

// Conectar a la base de datos
connection.connect((err) => {
    if(err)throw err
    console.log("conexion exitosa con universidad")
});





// 1. Seleccionar todas las carreras
function seleccionarTodasLasCarreras() {
    connection.query('SELECT * FROM carrera', (err, results) => {
        if(err){
            throw err
        }else{
            console.log('Carreras:', results);
        }
    
    });
}

// 2. Seleccionar una carrera específica por su código
function seleccionarCarreraPorCodigo(codigo) {
    connection.query('SELECT * FROM carrera WHERE codigo = ?', [codigo], (err, results) => {
        if(err){
            throw err
        }else{
            console.log('Carreras:', results);
        }
    });
}

// 3. Agregar una nueva carrera
function agregarCarrera(codigo, nombre,universidad,modalidad_id) {
    connection.query('INSERT INTO carrera (codigo, nombre , universidad ,modalidad_id) VALUES (?, ? , ? , ?)', [codigo, nombre,universidad,modalidad_id], (err, result) => {
        if(err){
            throw err
        }else{
            console.log("carrera agregada con exito")
        }
    });
}

// 4. Actualizar el nombre de una carrera dado su código
function actualizarNombreCarrera(codigo, nuevoNombre) {
    connection.query('UPDATE carrera SET nombre = ? WHERE codigo = ?', [nuevoNombre, codigo], (err, result) => {
        if(err){
            throw err
        }else{
            console.log("carrera Actualizada con exito")
        }
    });
}

// 5. Eliminar una carrera dado su id
function eliminarCarreraPorId(id) {
    connection.query('DELETE FROM carrera WHERE id = ?', [id], (err, result) => {
        if(err){
            throw err
        }else{
            console.log("carrera eliminada  con exito")
        }
    });
}

// 6. Contar el número total de registros en la tabla carrera
function contarCarreras() {
    connection.query('SELECT COUNT(*) AS total FROM carrera', (err, results) => {
        if (err) throw err;
        console.log('Número total de carreras:', results[0].total);
    });
}

//seleccionarTodasLasCarreras()
//seleccionarCarreraPorCodigo("INGC001")
//agregarCarrera("INGS001","Ingenieria en Sistemas","UTPL",1)
//actualizarNombreCarrera("INGC001","Ingenieria Informatica")
//eliminarCarreraPorId(2)
//contarCarreras()

connection.end();
