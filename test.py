def write_polyfit_calibration(date_str, comment, grating, ID_mode, breakpoints, cal, **kwargs):
    """
    Write calibration entry for a given grating, mode, and breakpoints using existing cal object.
    """
    import numpy as np
    from iexcode.instruments.utilities import today
    from os.path import join

    # Handle optional args
    kwargs.setdefault("poly_rank", 1)
    kwargs.setdefault("filename", IDcal_fname)
    kwargs.setdefault("path", dictionary_path)
    kwargs.setdefault("debug", False)

    # Basic error checks
    if cal is None:
        raise ValueError("Calibration object 'cal' is None.")
    if len(breakpoints) < 1:
        raise ValueError("Must supply at least one breakpoint.")
    if len(cal.id_sp_eV) < 2:
        raise ValueError("Not enough data points in calibration.")

    # Format the date
    date_fmt = "".join(date_str.split("/")[::-1])  # "06/04/2025" → "20250604"

    # Prepare ID calibration dictionary entry
    entry = {grating: {ID_mode: []}}

    hv_array = np.array(cal.mono_max)
    id_array = np.array(cal.id_sp_eV)

    break_indices = [0]
    for bp in breakpoints:
        # Find the index in hv_array closest to bp
        if bp > max(hv_array):
            continue  # skip if breakpoint outside range
        idx = np.argmin(np.abs(hv_array - bp))
        break_indices.append(idx)
    break_indices.append(len(hv_array))

    if kwargs['debug']:
        print("Break indices:", break_indices)

    # Compute fits
    for i in range(len(break_indices)-1):
        i1, i2 = break_indices[i], break_indices[i+1]
        if i2 - i1 < kwargs['poly_rank'] + 1:
            print(f"Skipping segment {i1}-{i2}: not enough points for poly rank {kwargs['poly_rank']}")
            continue
        try:
            hv_seg = hv_array[i1:i2]
            id_seg = id_array[i1:i2]
            coefs = list(np.polynomial.polynomial.polyfit(hv_seg, id_seg, kwargs['poly_rank']))
            bp_val = round(hv_seg[0], 2)
            entry[grating][ID_mode].append([bp_val, coefs])
        except Exception as e:
            print(f"Error fitting segment {i1}-{i2}: {e}")
            continue

    # Write to file
    fpath = join(kwargs['path'], kwargs['filename'])
    print(f"\nSaving calibration to: {fpath}")
    with open(fpath, "a+") as f:
        f.write(f"\n======= {date_fmt}: {comment}\n")
        f.write(str(entry) + "\n")

    if kwargs["debug"]:
        print("Final entry written:", entry)
