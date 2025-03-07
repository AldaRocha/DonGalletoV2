using Microsoft.AspNetCore.Mvc;
using Security;
using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Entidad.ViewModel;
using System.Collections.Generic;
using System;
using Servicios.Fachada.CQRS;

namespace Servicios.Fachada.Controllers.v1.Sistema
{
    [Route("api/v1/receta")]
    public class RecetaController : ControllerBase
    {
        AccesoDatos DbContext;
        Response response;

        public RecetaController(AccesoDatos DbContext)
        {
            this.DbContext = DbContext;
            this.response = new Response();
        }

        [HttpGet("{GalletaId}")]
        public ActionResult<Response> GetReceta(int GalletaId)
        {
            try
            {
                RecetaCQRS rcqrs = new RecetaCQRS();
                List<Receta> lista = rcqrs.GetReceta(DbContext, GalletaId);
                List<RecetaViewModel> dataList = new List<RecetaViewModel>();

                if (lista != null)
                {
                    foreach (Receta r in lista)
                    {
                        MedidaViewModel modelMedida = new MedidaViewModel();
                        GalletaViewModel modelGalleta = new GalletaViewModel();
                        InventarioViewModel modelInventario = new InventarioViewModel();
                        RecetaViewModel model = new RecetaViewModel();

                        modelMedida.id = r.Medida.MedidaId;
                        modelMedida.nombre = r.Medida.Nombre;

                        modelGalleta.id = r.Galleta.GalletaId;
                        modelGalleta.nombre = r.Galleta.Nombre;
                        modelGalleta.cantidad = r.Galleta.Cantidad;
                        modelGalleta.precioVenta = r.Galleta.PrecioVenta;
                        modelGalleta.precioProduccion = r.Galleta.PrecioProduccion;
                        modelGalleta.imagen = r.Galleta.Imagen;
                        modelGalleta.pesoGalleta = r.Galleta.PesoGalleta;
                        modelGalleta.idMedida = r.Galleta.MedidaId;

                        modelInventario.id = r.Inventario.InventarioId;
                        modelInventario.nombre = r.Inventario.Nombre;
                        modelInventario.fechaCompra = r.Inventario.FechaCompra.ToString();
                        modelInventario.fechaVencimiento = r.Inventario.FechaVencimiento.ToString();
                        modelInventario.activo = r.Inventario.Activo;
                        modelInventario.cantidad = r.Inventario.Cantidad;
                        modelInventario.precio = r.Inventario.Precio;
                        modelInventario.porcentaje = r.Inventario.Porcentaje;
                        modelInventario.proveedor = r.Inventario.Proveedor;
                        modelInventario.idMedida = r.Inventario.MedidaId;

                        model.id = r.RecetaId;
                        model.cantidad = r.Cantidad;
                        model.idGalleta = r.GalletaId;
                        model.galleta = modelGalleta;
                        model.idInventario = r.InventarioId;
                        model.inventario = modelInventario;
                        model.idMedida = r.MedidaId;
                        model.medida = modelMedida;

                        dataList.Add(model);
                    }
                }

                return response.Ok("", dataList);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }
    }
}
