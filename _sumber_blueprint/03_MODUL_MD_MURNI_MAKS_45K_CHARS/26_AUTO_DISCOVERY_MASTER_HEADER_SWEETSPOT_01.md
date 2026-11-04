
<!-- [ID:26_AUTO_DISCOVERY_MASTER_HEADER_S001] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: MASTER_HEADER -->
## Halaman 13

    master_part = 1​
    curr_master_text = [master_header]​
    curr_master_len = len(master_header)​
​
    for entry in master_catalog_entries:​
        lines = [f"\n## 📁 FILE MODUL: `{entry['file']}` 
({entry['chars']:,} karakter)\n"]​
        for it in entry["items"]:​
            sym_str = f" | Kode/Fungsi: `{', 
'.join(it['symbols'][:6])}`" if it["symbols"] else ""​
            img_str = f" | Gambar: `{', '.join(it['images'][:3])}`" if 
it["images"] else ""​
            tag_str = f" | Label: `{', '.join(it['tags'])}`" if 
it["tags"] else ""​
            lines.append(​
                f"- **[{it['id']}]** {it['title']} ({it['chars']:,} 
chr | *{it['grade']}*{sym_str}{img_str}{tag_str})\n"​
            )​
        block_str = "".join(lines)​
​
        # Jika mendekati batas Sweetspot 45.000 karakter, simpan dan 
buka File Master berikutnya​
        if curr_master_len + len(block_str) > MAX_MD_SWEETSPOT_CHARS 
and curr_master_text:​
            m_name = f"00_MASTER_PETA_OTAK_PART_{master_part:02d}.md"​
            (MASTER_BLUEPRINT / 
m_name).write_text("".join(curr_master_text), encoding="utf-8")​
            master_part += 1​
            curr_master_text = [master_header + f"*(Lanjutan Bagian 
{master_part})*\n\n"]​
            curr_master_len = len(curr_master_text[0])​
​
        curr_master_text.append(block_str)​
        curr_master_len += len(block_str)​
​
    if curr_master_text:​
        m_name = f"00_MASTER_PETA_OTAK_PART_{master_part:02d}.md"​
        (MASTER_BLUEPRINT / 
m_name).write_text("".join(curr_master_text), encoding="utf-8")​
​
    
print("\n=============================================================
=========")​
    print("✅ EKSEKUSI SELESAI! BUKTI KEUTUHAN DATA (100% LOSSLESS):")​
    print(f"   - Total Karakter Mentah Masuk       : 
{total_input_chars:,} karakter")​
    print(f"   - Duplikat Kembar 100% (SHA-256)    : 
{exact_dup_chars:,} karakter")​


