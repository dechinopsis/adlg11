&Pgcod = 1
&Trmod = 666

Do 'Get transaction number'

&Trnom = 'GenAI defined'

&AccountinEntryJson.FromJson(&AccountinEntryJSONString)
//&Trnro = &AccountinEntryJson.Get(!"nro")
//&Trnom = &AccountinEntryJson.Get(!"nombre")
&ordinalsJson.FromJson(&AccountinEntryJson.Get(!"ordinals"))

Do 'Clear existent entry'

New //--FST034
Pgcod  = &Pgcod
Trmod  = &Trmod
Trnro  = &Trnro
Trnom  = &Trnom
Trhabt = 'N'
Trtext = 'N'
Trmn   = 'N'
Trme   = 'N'
Trreco = 'N'
Tropau = 'N'
Tromlm = 'N'
Trimpr = 'N'
Trcej  = 'N'
Trincr = 'S'
Trbjpa = 'S'
Trbjan = 'S'
Trccla = 'N'
Trnetp = 'N'
Triva  = 'N'
Trdtpo = 'N'
Trconf = 'S'
EndNew


For &ordinal in &ordinalsJson
    &Trord   = &ordinal.Get(!"nro").ToNumeric()
    &debeHab = &ordinal.Get(!"debe_hab")
	&Trdh = IIF(&debeHab = "db", 1, 2)

    &sucursalJson.FromJson(&ordinal.Get(!"sucursal"))
    &sucursalTipo = &sucursalJson.Get(!"tipo")

	&Trpsuc = 'M'
	&Trasuc = 0
	&Trfsuc = 0
    Do Case
        Case &sucursalTipo = "sucursal matriz"
            &Trpsuc = 'M'
        Case &sucursalTipo = "sucursal de trabajo"
            &Trpsuc = 'N'
        Case &sucursalTipo = "solicitar"
            &Trpsuc = 'S'
        Case &sucursalTipo = "solicitar sugiriendo la de trabajo"
            &Trpsuc = 'B'
        Case &sucursalTipo = "forzar valor"
            &Trpsuc = 'F'
            &Trfsuc = &sucursalJson.Get(!"valor").ToNumeric()
        Case &sucursalTipo = "obtener de ordinal anterior"
            &Trpsuc = 'A'
            &Trasuc = &sucursalJson.Get(!"ordinal_nro").ToNumeric()
        Case &sucursalTipo = "obtener de la cuenta"
            &Trpsuc = 'C'
        Case &sucursalTipo = "capturar por medio externo"
            &Trpsuc = 'E'
        Case &sucursalTipo = "obtener del preformato"
            &Trpsuc = 'P'
            &Trasuc = &sucursalJson.Get(!"preformato_nro").ToNumeric()
        Case &sucursalTipo = "obtener del preformato y pedir"
            &Trpsuc = 'Q'
            &Trasuc = &sucursalJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &especieJson.FromJson(&ordinal.Get(!"especie"))
    &especieTipo = &especieJson.Get(!"tipo")
	&Trppap = 'N'
	&Trapap = 0
	&Trfpap = 0
    Do Case
        Case &especieTipo = "no corresponde"
            &Trppap = 'N'
        Case &especieTipo = "solicitar"
            &Trppap = 'S'
        Case &especieTipo = "forzar valor"
            &Trppap = 'F'
            &Trfpap = &especieJson.Get(!"valor").ToNumeric()
        Case &especieTipo = "obtener de ordinal anterior"
            &Trppap = 'A'
            &Trapap = &especieJson.Get(!"ordinal_nro").ToNumeric()
        Case &especieTipo = "obtener del preformato"
            &Trppap = 'P'
            &Trapap = &especieJson.Get(!"preformato_nro").ToNumeric()
        Case &especieTipo = "obtener del preformato y pedir"
            &Trppap = 'Q'
            &Trapap = &especieJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &monedaJson.FromJson(&ordinal.Get(!"moneda"))
    &monedaTipo = &monedaJson.Get(!"tipo")
	&Trpmda = 'N'
	&Tramda = 0
	&Trfmda = 0
    Do Case
        Case &monedaTipo = "no corresponde"
            &Trpmda = 'N'
        Case &monedaTipo = "solicitar"
            &Trpmda = 'S'
        Case &monedaTipo = "forzar valor"
            &Trpmda = 'F'
            &Trfmda = &monedaJson.Get(!"valor").ToNumeric()
        Case &monedaTipo = "obtener de ordinal anterior"
            &Trpmda = 'A'
            &Tramda = &monedaJson.Get(!"ordinal_nro").ToNumeric()
        Case &monedaTipo = "obtener del preformato"
            &Trpmda = 'P'
            &Tramda = &monedaJson.Get(!"preformato_nro").ToNumeric()
        Case &monedaTipo = "obtener del preformato y pedir"
            &Trpmda = 'Q'
            &Tramda = &monedaJson.Get(!"preformato_nro").ToNumeric()
        Case &monedaTipo = "capturar por medio externo"
            &Trpmda = 'E'
        Case &monedaTipo = "forzar moneda nacional"
            &Trpmda = 'M'
        Case &monedaTipo = "forzar moneda extranjera"
            &Trpmda = 'D'
    EndCase

    &cuentaJson.FromJson(&ordinal.Get(!"cuenta"))
    &cuentaTipo = &cuentaJson.Get(!"tipo")
	&Trpcta = 'N'
	&Tracta = 0
	&Trfcta = 0
    Do Case
        Case &cuentaTipo = "no corresponde"
            &Trpcta = 'N'
        Case &cuentaTipo = "solicitar"
            &Trpcta = 'S'
        Case &cuentaTipo = "forzar valor"
            &Trpcta = 'F'
            &Trfcta = &cuentaJson.Get(!"valor").ToNumeric()
        Case &cuentaTipo = "obtener de ordinal anterior"
            &Trpcta = 'A'
            &Tracta = &cuentaJson.Get(!"ordinal_nro").ToNumeric()
        Case &cuentaTipo = "obtener de ordinal anterior y pedir"
            &Trpcta = 'B'
            &Tracta = &cuentaJson.Get(!"ordinal_nro").ToNumeric()
        Case &cuentaTipo = "obtener del preformato"
            &Trpcta = 'P'
            &Tracta = &cuentaJson.Get(!"preformato_nro").ToNumeric()
        Case &cuentaTipo = "obtener del preformato y pedir"
            &Trpcta = 'Q'
            &Tracta = &cuentaJson.Get(!"preformato_nro").ToNumeric()
        Case &cuentaTipo = "capturar por medio externo"
            &Trpcta = 'E'
    EndCase

    &nroOperacionJson.FromJson(&ordinal.Get(!"nroOperacion"))
    &nroOperacionTipo = &nroOperacionJson.Get(!"tipo")
	&Trpop = 'N'
	&Traop = 0
	&Trfop = 0
    Do Case
        Case &nroOperacionTipo = "no corresponde"
            &Trpop = 'N'
        Case &nroOperacionTipo = "solicitar"
            &Trpop = 'S'
        Case &nroOperacionTipo = "forzar valor"
            &Trpop = 'F'
            &Trfop = &nroOperacionJson.Get(!"valor").ToNumeric()
        Case &nroOperacionTipo = "obtener de ordinal anterior"
            &Trpop = 'A'
            &Traop = &nroOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &nroOperacionTipo = "automatica por sucursal"
            &Trpop = 'U'
        Case &nroOperacionTipo = "automatica por modulo"
            &Trpop = 'M'
        Case &nroOperacionTipo = "obtener del preformato"
            &Trpop = 'P'
            &Traop = &nroOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &nroOperacionTipo = "obtener del preformato y pedir"
            &Trpop = 'Q'
            &Traop = &nroOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &nroOperacionTipo = "resuelve con fecha valor"
            &Trpop = 'B'
        Case &nroOperacionTipo = "resuelve con fecha valor contable"
            &Trpop = 'V'
        Case &nroOperacionTipo = "resuelve con fecha de contabilización"
            &Trpop = 'I'
    EndCase

    &subOperacionJson.FromJson(&ordinal.Get(!"subOperacion"))
    &subOperacionTipo = &subOperacionJson.Get(!"tipo")
	&Trpsop = 'N'
	&Trasop = 0
	&Trfsop = 0
    Do Case
        Case &subOperacionTipo = "no corresponde"
            &Trpsop = 'N'
        Case &subOperacionTipo = "solicitar"
            &Trpsop = 'S'
        Case &subOperacionTipo = "forzar valor"
            &Trpsop = 'F'
            &Trfsop = &subOperacionJson.Get(!"valor").ToNumeric()
        Case &subOperacionTipo = "obtener de ordinal anterior"
            &Trpsop = 'A'
            &Trasop = &subOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &subOperacionTipo = "obtener de ordinal anterior e incrementar"
            &Trpsop = 'B'
            &Trasop = &subOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &subOperacionTipo = "forzar nro de caja"
            &Trpsop = 'C'
        Case &subOperacionTipo = "obtener del preformato"
            &Trpsop = 'P'
            &Trasop = &subOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &subOperacionTipo = "obtener del preformato y pedir"
            &Trpsop = 'Q'
            &Trasop = &subOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &subOperacionTipo = "capturar por medio externo"
            &Trpsop = 'E'
        Case &subOperacionTipo = "resuelve con nro de relación"
            &Trpsop = 'H'
    EndCase

    &tipoOperacionJson.FromJson(&ordinal.Get(!"tipoOperacion"))
    &tipoOperacionTipo = &tipoOperacionJson.Get(!"tipo")
	&Trptop = 'N'
	&Tratop = 0
	&Trftop = 0
    Do Case
        Case &tipoOperacionTipo = "no corresponde"
            &Trptop = 'N'
        Case &tipoOperacionTipo = "tratamiento automatico"
            &Trptop = Chr(0)
        Case &tipoOperacionTipo = "forzar valor"
            &Trptop = 'F'
            &Trftop = &tipoOperacionJson.Get(!"valor").ToNumeric()
        Case &tipoOperacionTipo = "obtener de ordinal anterior"
            &Trptop = 'A'
            &Tratop = &tipoOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &tipoOperacionTipo = "obtener del preformato"
            &Trptop = 'P'
            &Tratop = &tipoOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &tipoOperacionTipo = "obtener del preformato y pedir"
            &Trptop = 'Q'
            &Tratop = &tipoOperacionJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &fechaValorJson.FromJson(&ordinal.Get(!"fechaValor"))
    &fechaValorTipo = &fechaValorJson.Get(!"tipo")
    &Trfval = 'N'
    &Traval = 0
    Do Case
        Case &fechaValorTipo = "no corresponde"
            &Trfval = 'N'
        Case &fechaValorTipo = "admite fecha valor pasado"
            &Trfval = 'P'
        Case &fechaValorTipo = "admite fecha valor futuro"
            &Trfval = 'F'
        Case &fechaValorTipo = "admite fecha valor pasado y/o futuro"
            &Trfval = 'I'
        Case &fechaValorTipo = "obtener de la operacion existente"
            &Trfval = 'E'
        Case &fechaValorTipo = "obtener de ordinal anterior"
            &Trfval = 'A'
            &Traval = &fechaValorJson.Get(!"ordinal_nro").ToNumeric()
        Case &fechaValorTipo = "forzar la fecha valor contable"
            &Trfval = 'C'
        Case &fechaValorTipo = "obtener del preformato"
            &Trfval = 'Q'
            &Traval = &fechaValorJson.Get(!"preformato_nro").ToNumeric()
        Case &fechaValorTipo = "obtener del preformato y pedir"
            &Trfval = 'R'
            &Traval = &fechaValorJson.Get(!"preformato_nro").ToNumeric()
        Case &fechaValorTipo = "vencimiento anterior"
            &Trfval = 'B'
    EndCase

    &fechaVtoJson.FromJson(&ordinal.Get(!"fechaVto"))
    &fechaVtoTipo = &fechaVtoJson.Get(!"tipo")
    &Trfvto = 'N'
    &Travto = 0
    Do Case
        Case &fechaVtoTipo = "no corresponde"
            &Trfvto = 'N'
        Case &fechaVtoTipo = "solicitar el plazo"
            &Trfvto = 'P'
        Case &fechaVtoTipo = "solicitar fecha de vencimiento"
            &Trfvto = 'V'
        Case &fechaVtoTipo = "solicitar el plazo y la fecha de vencimiento"
            &Trfvto = 'I'
        Case &fechaVtoTipo = "obtener de la operacion existente"
            &Trfvto = 'E'
        Case &fechaVtoTipo = "obtener de ordinal anterior"
            &Trfvto = 'A'
            &Travto = &fechaVtoJson.Get(!"ordinal_nro").ToNumeric()
        Case &fechaVtoTipo = "se resuelve en una RTE"
            &Trfvto = 'R'
        Case &fechaVtoTipo = "obtener del preformato"
            &Trfvto = 'S'
            &Travto = &fechaVtoJson.Get(!"preformato_nro").ToNumeric()
        Case &fechaVtoTipo = "obtener plazo del preformato"
            &Trfvto = 'Q'
            &Travto = &fechaVtoJson.Get(!"preformato_nro").ToNumeric()
        Case &fechaVtoTipo = "obtener fecha valor anterior"
            &Trfvto = 'F'
        Case &fechaVtoTipo = "obtener de fecha valor"
            &Trfvto = 'B'
        Case &fechaVtoTipo = "forzar fecha valor contable"
            &Trfvto = 'C'
        Case &fechaVtoTipo = "forzar fecha de contabilizacion"
            &Trfvto = 'D'
        Case &fechaVtoTipo = "obtener plazo de la operacion existente"
            &Trfvto = 'G'
    EndCase

    &importeJson.FromJson(&ordinal.Get(!"importe"))
    &importeTipo = &importeJson.Get(!"tipo")
    &Trpimp = 'S'
    &Traimp = 0
    Do Case
        Case &importeTipo = "solicitar"
            &Trpimp = 'S'
        Case &importeTipo = "obtener de ordinal anterior"
            &Trpimp = 'A'
            &Traimp = &importeJson.Get(!"ordinal_nro").ToNumeric()
        Case &importeTipo = "obtener de ordinal anterior y pedir"
            &Trpimp = 'B'
            &Traimp = &importeJson.Get(!"ordinal_nro").ToNumeric()
        Case &importeTipo = "obtener de saldo de la operacion existente"
            &Trpimp = 'E'
        Case &importeTipo = "obtener de saldo de la operacion existente y pedir"
            &Trpimp = 'F'
        Case &importeTipo = "obtener del preformato"
            &Trpimp = 'P'
            &Traimp = &importeJson.Get(!"preformato_nro").ToNumeric()
        Case &importeTipo = "obtener del preformato y pedir"
            &Trpimp = 'Q'
            &Traimp = &importeJson.Get(!"preformato_nro").ToNumeric()
        Case &importeTipo = "se resuelve en una RTE"
            &Trpimp = 'R'
    EndCase

	New //--FST035
	Pgcod    = &Pgcod
	Trmod    = &Trmod
	Trnro    = &Trnro
	Trord    = &Trord
	Trdh     = &Trdh
	Trordhab = 'S'
	Trpsuc   = &Trpsuc
	Trasuc   = &Trasuc
	Trfsuc   = &Trfsuc
	Trppap   = &Trppap
	Trapap   = &Trapap
	Trfpap   = &Trfpap
	Trpmda   = &Trpmda
	Tramda   = &Tramda
	Trfmda   = &Trfmda
	Trpcta   = &Trpcta
	Tracta   = &Tracta
	Trfcta   = &Trfcta
	Trpop    = &Trpop
	Traop    = &Traop
	Trfop    = &Trfop
	Trpsop   = &Trpsop
	Trasop   = &Trasop
	Trfsop   = &Trfsop
	Trptop   = &Trptop
	Tratop   = &Tratop
	Trftop   = &Trftop
	Trfval   = &Trfval
	Traval   = &Traval
	Trfvto   = &Trfvto
	Travto   = &Travto
	Trpimp   = &Trpimp
	Traimp   = &Traimp
	EndNew

    Do 'Add subordinal'
Endfor

Sub 'Add subordinal'
    &rubroJson.FromJson(&ordinal.Get(!"rubro"))
    &rubroTipo = &rubroJson.Get(!"tipo")
	&Trrubr    = 0
	&Trrcod    = 0
	&Trrord    = 0

    If &rubroTipo = "valor"
        &Trrubr = &rubroJson.Get(!"rubro").ToNumeric()
    Else // "relacionado"
        &Trrord = &rubroJson.Get(!"fromOrdinal").ToNumeric()
        &Trrcod = &rubroJson.Get(!"relCode").ToNumeric()
    EndIf

	&Trsbor = 10

	New //--FST036
	Pgcod  = &Pgcod
	Trmod  = &Trmod
	Trnro  = &Trnro
	Trord  = &Trord
	Trsbor = &Trsbor
	Trrubr = &Trrubr
	Trrcod = &Trrcod
	Trrord = &Trrord
	EndNew

EndSub

Sub 'Clear existent entry'
    For Each //--FST034
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Where Trnro = &Trnro
	Defined by Trnom
		Delete
    EndFor

    For Each //--FST035
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Where Trnro = &Trnro
	Defined by Trdh
		Delete
    EndFor

    For Each //--FST036
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Where Trnro = &Trnro
	Defined by Trrubr
		Delete
    EndFor
EndSub

Sub 'Get transaction number'
    &Trnro = 0
    For Each Order Pgcod, Trmod, Trnro //--FST034
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Defined by Trnom
		&Trnro = Trnro
    EndFor

    &Trnro = &Trnro + 1
EndSub