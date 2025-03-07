using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Fachada.DAO;
using System;
using System.Collections.Generic;

namespace Servicios.Fachada.CQRS
{
    public class RecetaCQRS
    {
        public List<Receta> GetReceta(AccesoDatos DbContext, int GalletaId)
        {
            try
            {
                if (GalletaId != null)
                {
                    RecetaDAO idao = new RecetaDAO();

                    return idao.GetReceta(DbContext, GalletaId);
                }
                else
                {
                    return null;
                }
            }
            catch (Exception ex)
            {
                return null;
            }
        }

        public string AgregarReceta(AccesoDatos DbContext, int GalletaId, List<Receta> dataList)
        {
            string mensaje = null;
            try
            {
                bool guardar = true;
                int i = 1;

                foreach (Receta receta in dataList)
                {
                    mensaje = i.ToString();

                    if (receta.Cantidad <= 0)
                    {
                        guardar = false;
                        break;
                    }

                    if (receta.GalletaId <= 0)
                    {
                        guardar = false;
                        break;
                    }

                    if (receta.InventarioId <= 0)
                    {
                        guardar = false;
                        break;
                    }

                    if (receta.MedidaId <= 0)
                    {
                        guardar = false;
                        break;
                    }

                    i++;
                }

                if (guardar)
                {
                    RecetaDAO idao = new RecetaDAO();

                    mensaje = idao.AgregarReceta(DbContext, GalletaId, dataList);
                }
                else
                {
                    mensaje = "La receta esta incompleta en la fila '" + mensaje + "'";
                }
            }
            catch (Exception ex)
            {
                mensaje = "No se pudo validar la lista en el cqrs por problemas con el producto: " + mensaje;
            }
            return mensaje;
        }
    }
}
