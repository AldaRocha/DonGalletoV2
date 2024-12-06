using Microsoft.AspNetCore.Mvc;
using Security;
using Servicios.Datos;
using Servicios.Entidad.ViewModel;
using Servicios.Fachada.AppService;
using System.Collections.Generic;
using System;
using Servicios.Fachada.DAO;
using Servicios.Entidad.Model;
using Servicios.Fachada.CQRS;

namespace Servicios.Fachada.Controllers.v1.Sistema
{
    [Route("api/v1/galleta")]
    public class GalletaController : ControllerBase
    {
        AccesoDatos DbContext;
        Response response;

        public GalletaController(AccesoDatos DbContext)
        {
            this.DbContext = DbContext;
            this.response = new Response();
        }

        [HttpGet]
        public ActionResult<Response> GetGalleta()
        {
            try
            {
                GalletaDAO gdao = new GalletaDAO();
                List<Galleta> lista = gdao.GetAllGalleta(DbContext);
                List<GalletaViewModel> dataList = new List<GalletaViewModel>();

                foreach (Galleta g in lista)
                {
                    GalletaViewModel model = new GalletaViewModel();
                    MedidaViewModel mvm = new MedidaViewModel();

                    mvm.id = g.Medida.MedidaId;
                    mvm.nombre = g.Medida.Nombre;

                    model.id = g.GalletaId;
                    model.nombre = g.Nombre;
                    model.cantidad = g.Cantidad;
                    model.precioVenta = g.PrecioVenta;
                    model.precioProduccion = g.PrecioProduccion;
                    model.imagen = g.Imagen;
                    model.pesoGalleta = g.PesoGalleta;
                    model.idMedida = g.MedidaId;
                    model.medida = mvm;

                    dataList.Add(model);
                }

                return response.Ok("", dataList);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpPost]
        public ActionResult<Response> AgregarGalleta([FromBody] RequestInterface request)
        {
            try
            {
                GalletaViewModel data = request.getData<GalletaViewModel>();
                GalletaCQRS gcqrs = new GalletaCQRS();
                Galleta galleta = new Galleta();

                galleta.Nombre = data.nombre;
                galleta.Cantidad = (decimal)data.cantidad;
                galleta.PrecioVenta = (decimal)data.precioVenta;
                galleta.PrecioProduccion = (decimal)data.precioProduccion;
                galleta.Imagen = data.imagen;
                galleta.PesoGalleta = (decimal)data.pesoGalleta;
                galleta.MedidaId = (int)data.idMedida;

                data.id = gcqrs.AgregarGalleta(DbContext, galleta);

                return response.Ok(null, data);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpPut]
        public ActionResult<Response> ActualizarGalleta([FromBody] RequestInterface request)
        {
            try
            {
                GalletaViewModel data = request.getData<GalletaViewModel>();
                GalletaCQRS gcqrs = new GalletaCQRS();
                RecetaCQRS rcqrs = new RecetaCQRS();
                Galleta galleta = new Galleta();
                List<Receta> receta = new List<Receta>();

                galleta.GalletaId = (int)data.id;
                galleta.Nombre = data.nombre;
                galleta.Cantidad = (decimal)data.cantidad;
                galleta.PrecioVenta = (decimal)data.precioVenta;
                galleta.PrecioProduccion = (decimal)data.precioProduccion;
                galleta.Imagen = data.imagen;
                galleta.PesoGalleta = (decimal)data.pesoGalleta;
                galleta.MedidaId = (int)data.idMedida;

                foreach (RecetaViewModel model in data.recetamodel)
                {
                    Receta r = new Receta();

                    r.Cantidad = (decimal)model.cantidad;
                    r.GalletaId = (int)model.idGalleta;
                    r.InventarioId = (int)model.idInventario;
                    r.MedidaId = (int)model.idMedida;

                    receta.Add(r);
                }

                string mensaje;
                string mensajeGalleta = gcqrs.ActualizarGalleta(DbContext, galleta);
                string mensajeReceta = rcqrs.AgregarReceta(DbContext, galleta.GalletaId, receta);

                if (mensajeGalleta == null && mensajeReceta == null)
                {
                    mensaje = null;
                }
                else
                {
                    if (mensajeGalleta == null)
                    {
                        mensaje = mensajeReceta;
                    }
                    else
                    {
                        mensaje = mensajeGalleta;
                    }
                }

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }
    }
}
