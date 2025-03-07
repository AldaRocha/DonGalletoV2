using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace Servicios.Entidad.Model
{
    public class Galleta
    {
        [Key]
        public int GalletaId { get; set; }
	    public string Nombre { get; set; }
        public decimal Cantidad { get; set; }
        public decimal PrecioVenta { get; set; }
        public decimal PrecioProduccion { get; set; }
        public string Imagen { get; set; }
        public decimal PesoGalleta { get; set; }
        public int MedidaId { get; set; }
        public virtual Medida Medida { get; set; }
    }
}
