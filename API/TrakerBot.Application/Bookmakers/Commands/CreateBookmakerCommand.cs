using AutoMapper;
using MediatR;
using TrakerBot.Application.Bookmakers.DTOs;
using TrakerBot.Application.Core;
using TrakerBot.Core.Entities;
using TrakerBot.Persistance;

namespace TrakerBot.Application.Bookmakers.Commands;

public class CreateBookmakerCommand
{
    public class Command : IRequest<Result<string>>
    {
        public required CreateBookmakerDto CreateBookmakerDto { get; set; }
    }

    public class Handler(ApplicationDbContext applicationDbContext, IMapper mapper) : IRequestHandler<Command, Result<string>>
    {
        public async Task<Result<string>> Handle(Command request, CancellationToken cancellationToken)
        {
            var bookmaker = mapper.Map<Bookmaker>(request.CreateBookmakerDto);
            bookmaker.CreatedAt = bookmaker.UpdatedAt = DateTime.UtcNow;

            applicationDbContext.Bookmakers.Add(bookmaker);
            
            return await applicationDbContext.SaveChangesAsync(cancellationToken) > 0
                ? Result<string>.Success(bookmaker.Id)
                : Result<string>.Failure("Failed to create bookmaker", 400);
        }
    }
}
