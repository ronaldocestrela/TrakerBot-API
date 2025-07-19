using AutoMapper;
using TrakerBot.Application.Bookmakers.DTOs;
using TrakerBot.Core.Entities;

namespace TrakerBot.Application.Core;

public class MappingProfiles : Profile
{
    public MappingProfiles()
    {
        CreateMap<CreateBookmakerDto, Bookmaker>().ReverseMap();
    }
}
