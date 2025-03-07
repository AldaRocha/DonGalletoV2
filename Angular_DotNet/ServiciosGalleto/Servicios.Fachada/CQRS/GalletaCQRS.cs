using DocumentFormat.OpenXml.Drawing;
using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Fachada.DAO;
using System;

namespace Servicios.Fachada.CQRS
{
    public class GalletaCQRS
    {
        public int AgregarGalleta(AccesoDatos DbContext, Galleta data)
        {
            try
            {
                bool guardar = true;

                if (data.Nombre == null || data.Nombre == "")
                {
                    guardar = false;
                }

                if (data.Cantidad < 0)
                {
                    guardar = false;
                }

                if (data.PrecioVenta == 0)
                {
                    guardar = false;
                }

                if (data.PrecioProduccion == 0)
                {
                    guardar = false;
                }

                if (data.Imagen == null || data.Imagen == "")
                {
                    guardar = false;
                }

                if (data.PesoGalleta == 0)
                {
                    guardar = false;
                }

                if (data.MedidaId == 0)
                {
                    guardar = false;
                }

                if (guardar)
                {
                    GalletaDAO gdao = new GalletaDAO();

                    return gdao.AgregarGalleta(DbContext, data);
                }
                else
                {
                    return 0;
                }
            }
            catch (Exception ex)
            {
                return 0;
            }
        }

        public string ActualizarGalleta(AccesoDatos DbContext, Galleta data)
        {
            string mensaje = null;
            try
            {
                bool guardar = true;

                if (data.Nombre == null || data.Nombre == "")
                {
                    guardar = false;
                }

                if (data.Cantidad == 0)
                {
                    guardar = false;
                }

                if (data.PrecioVenta == 0)
                {
                    guardar = false;
                }

                if (data.PrecioProduccion == 0)
                {
                    guardar = false;
                }

                if (data.Imagen == null || data.Imagen == "")
                {
                    guardar = false;
                }

                if (data.PesoGalleta == 0)
                {
                    guardar = false;
                }

                if (data.MedidaId == 0)
                {
                    guardar = false;
                }

                if (guardar)
                {
                    GalletaDAO gdao = new GalletaDAO();

                    mensaje = gdao.ActualizarGalleta(DbContext, data);
                }
                else
                {
                    mensaje = "Al menos un dato de la galleta esta vacio.";
                }
            }
            catch (Exception ex)
            {
                mensaje = "No se pudo validar la galleta en el cqrs";
            }
            return mensaje;
        }
    }
}
