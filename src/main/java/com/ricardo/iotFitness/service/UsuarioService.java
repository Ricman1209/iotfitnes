package com.ricardo.iotFitness.service;

import com.ricardo.iotFitness.model.Usuario;
import com.ricardo.iotFitness.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;

    public UsuarioService(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    public Usuario crear(Usuario usuario) {
        return usuarioRepository.save(usuario);
    }

    public Usuario obtenerPorId(Integer id) {
        return usuarioRepository.findById(id).orElse(null);
    }

    public List<Usuario> obtenerTodos() {
        return usuarioRepository.findAll();
    }

    public Usuario actualizar(Integer id, Usuario usuario) {
        Usuario original = usuarioRepository.findById(id).orElse(null);
        if (original == null) return null;

        original.setNombres(usuario.getNombres());
        original.setApellidos(usuario.getApellidos());
        original.setEmail(usuario.getEmail());
        original.setFechaNacimiento(usuario.getFechaNacimiento());
        original.setGenero(usuario.getGenero());

        return usuarioRepository.save(original);
    }

    public void eliminar(Integer id) {
        usuarioRepository.deleteById(id);
    }
}