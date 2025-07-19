using MediatR;
using Microsoft.AspNetCore.Mvc;
using TrakerBot.Application.Core;

namespace TrakerBot.API.Controllers;

[Route("api/[controller]")]
[ApiController]
public class BaseApiController : ControllerBase
{
    private IMediator? _mediator;

    protected IMediator Mediator => _mediator ??= HttpContext.RequestServices.GetService<IMediator>()
        ?? throw new InvalidOperationException("IMediator service is unavailable");

    protected ActionResult<T> HandleResult<T>(Result<T> result)
    {
        if (!result. IsSuccess && result.Code == 404) return NotFound();
        if (result.IsSuccess && result.Data != null) return Ok(result.Data);
        if (result.IsSuccess && result.Data == null) return NoContent();
        return BadRequest(result.Error);
    }
}
